from typing import Literal

class RouterAgent:
    """
    Routes user queries to appropriate specialized agent.
    Uses simple keyword-based routing logic.
    """
    
    # Keywords that indicate data analysis queries
    DATA_KEYWORDS = [
        'total', 'sum', 'average', 'mean', 'count', 'how many',
        'calculate', 'compute', 'budget', 'cost', 'expense',
        'revenue', 'sales', 'profit', 'max', 'min', 'highest',
        'lowest', 'anomaly', 'outlier', 'trend', 'statistics'
    ]
    
    @staticmethod
    def route(query: str, available_files: dict) -> Literal['document_qa', 'data_analysis']:
        """
        Determine which agent should handle the query.
        
        Args:
            query: User's question
            available_files: Dict with 'documents' and 'data' file lists
            
        Returns:
            Agent type: 'document_qa' or 'data_analysis'
        """
        query_lower = query.lower()
        
        # Check if any data analysis keywords are present
        has_data_keywords = any(keyword in query_lower for keyword in RouterAgent.DATA_KEYWORDS)
        
        # Check what files are available
        has_documents = len(available_files.get('documents', [])) > 0
        has_data = len(available_files.get('data', [])) > 0
        
        # Routing logic:
        # 1. If data keywords present AND data files available -> data_analysis
        # 2. If only data files available -> data_analysis
        # 3. Otherwise -> document_qa
        
        if has_data_keywords and has_data:
            return 'data_analysis'
        elif has_data and not has_documents:
            return 'data_analysis'
        else:
            return 'document_qa'
    
    @staticmethod
    def get_routing_explanation(agent_type: str) -> str:
        """Get human-readable explanation of routing decision"""
        explanations = {
            'document_qa': 'Routed to Document Q&A Agent (PDF analysis)',
            'data_analysis': 'Routed to Data Analysis Agent (CSV/Excel analysis)'
        }
        return explanations.get(agent_type, 'Unknown agent')
