import os
import shutil
from typing import List
from fastapi import UploadFile
from pypdf import PdfReader
import pandas as pd

class FileHandler:
    """
    Handles file upload, validation, and content extraction.
    Supports PDF, CSV, and Excel formats.
    """
    
    ALLOWED_EXTENSIONS = {'.pdf', '.csv', '.xlsx', '.xls'}
    
    @staticmethod
    def validate_file(filename: str) -> bool:
        """Check if file extension is allowed"""
        ext = os.path.splitext(filename)[1].lower()
        return ext in FileHandler.ALLOWED_EXTENSIONS
    
    @staticmethod
    async def save_upload(file: UploadFile, upload_dir: str) -> str:
        """
        Save uploaded file to disk.
        Returns the full file path.
        """
        if not FileHandler.validate_file(file.filename):
            raise ValueError(f"File type not supported: {file.filename}")
        
        file_path = os.path.join(upload_dir, file.filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return file_path
    
    @staticmethod
    def extract_pdf_text(file_path: str) -> str:
        """
        Extract text content from PDF file.
        Returns concatenated text from all pages.
        """
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    
    @staticmethod
    def load_dataframe(file_path: str) -> pd.DataFrame:
        """
        Load CSV or Excel file into pandas DataFrame.
        Automatically detects file type by extension.
        """
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.csv':
            return pd.read_csv(file_path)
        elif ext in ['.xlsx', '.xls']:
            return pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported data file type: {ext}")
    
    @staticmethod
    def get_file_type(filename: str) -> str:
        """Determine if file is document (PDF) or data (CSV/Excel)"""
        ext = os.path.splitext(filename)[1].lower()
        if ext == '.pdf':
            return 'document'
        elif ext in ['.csv', '.xlsx', '.xls']:
            return 'data'
        return 'unknown'
