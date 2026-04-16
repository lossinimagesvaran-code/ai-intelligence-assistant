from typing import Dict, Any
from services.data_analyzer import DataAnalyzer

class DataAnalysisAgent:
    """
    Specialized agent for analyzing CSV/Excel data.
    Uses pandas for computation and LLM for explanation.
    """
    
    def __init__(self):
        """Initialize data analyzer"""
        self.analyzer = DataAnalyzer()
    
    def process_data_file(self, file_path: str, filename: str):
        """
        Load data file for analysis.
        
        Args:
            file_path: Path to CSV/Excel file
            filename: Original filename
        """
        self.analyzer.load_data(file_path, filename)
    
    def answer(self, query: str, conversation_history: list = None) -> Dict[str, Any]:
        """
        Answer analytical question about data.
        
        Args:
            query: User question
            conversation_history: Previous conversation turns
            
        Returns:
            Dict with answer, analysis results, and agent info
        """
        result = self.analyzer.analyze(query)
        
        return {
            "answer": result["answer"],
            "analysis": result.get("analysis"),
            "source": result.get("source"),
            "agent": "Data Analysis Agent",
            "agent_type": "data_analysis"
        }
