from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Dict, Any
from utils.file_handler import FileHandler
from agents.document_qa_agent import DocumentQAAgent
from agents.data_analysis_agent import DataAnalysisAgent
from config import settings
import os

router = APIRouter()

# Initialize agents (shared across requests)
doc_agent = DocumentQAAgent()
data_agent = DataAnalysisAgent()

# Track uploaded files
uploaded_files = {
    'documents': [],  # PDF files
    'data': []        # CSV/Excel files
}

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Upload and process PDF, CSV, or Excel files.
    
    Args:
        file: Uploaded file
        
    Returns:
        Success message with file info
    """
    try:
        # Validate file type
        if not FileHandler.validate_file(file.filename):
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Allowed: PDF, CSV, XLSX, XLS"
            )
        
        # Save file
        file_path = await FileHandler.save_upload(file, settings.upload_dir)
        file_type = FileHandler.get_file_type(file.filename)
        
        # Process based on file type
        if file_type == 'document':
            # Extract and index PDF
            text = FileHandler.extract_pdf_text(file_path)
            doc_agent.process_document(text, file.filename)
            uploaded_files['documents'].append(file.filename)
            message = f"PDF '{file.filename}' uploaded and indexed successfully"
            
        elif file_type == 'data':
            # Load data file
            data_agent.process_data_file(file_path, file.filename)
            uploaded_files['data'].append(file.filename)
            message = f"Data file '{file.filename}' uploaded and loaded successfully"
            
        else:
            raise HTTPException(status_code=400, detail="Unknown file type")
        
        return {
            "success": True,
            "message": message,
            "filename": file.filename,
            "file_type": file_type,
            "uploaded_files": uploaded_files
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@router.get("/files")
async def list_files() -> Dict[str, Any]:
    """
    List all uploaded files.
    
    Returns:
        Dict with document and data file lists
    """
    return {
        "uploaded_files": uploaded_files
    }

# Export agents and file tracker for use in query route
def get_agents():
    """Get initialized agents"""
    return doc_agent, data_agent

def get_uploaded_files():
    """Get uploaded files tracker"""
    return uploaded_files
