from typing import Dict, Any
from services.rag_pipeline import RAGPipeline

class DocumentQAAgent:
    """
    Specialized agent for answering questions about PDF documents.
    Uses RAG pipeline for retrieval and generation.
    """
    
    def __init__(self):
        """Initialize RAG pipeline"""
        self.rag_pipeline = RAGPipeline()
    
    def process_document(self, text: str, filename: str):
        """
        Index a document for future queries.
        
        Args:
            text: Full document text
            filename: Source filename
        """
        self.rag_pipeline.index_document(text, filename)
    
    def answer(self, query: str, conversation_history: list = None) -> Dict[str, Any]:
        """
        Answer question about documents using RAG.
        
        Args:
            query: User question
            conversation_history: Previous conversation turns (for context)
            
        Returns:
            Dict with answer, sources, and agent info
        """
        # For follow-up questions, we could incorporate conversation history
        # For simplicity, we'll use the query as-is
        
        result = self.rag_pipeline.query(query)
        
        return {
            "answer": result["answer"],
            "sources": result["sources"],
            "agent": "Document Q&A Agent",
            "agent_type": "document_qa"
        }
