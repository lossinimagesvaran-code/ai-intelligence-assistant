from typing import List, Dict, Any
from datetime import datetime

class ConversationManager:
    """
    Manages conversation history and context.
    Simple session-based memory implementation.
    """
    
    def __init__(self):
        """Initialize conversation storage"""
        self.sessions = {}  # session_id -> conversation history
    
    def create_session(self, session_id: str = None) -> str:
        """
        Create new conversation session.
        
        Args:
            session_id: Optional custom session ID
            
        Returns:
            Session ID
        """
        if session_id is None:
            session_id = f"session_{datetime.now().timestamp()}"
        
        self.sessions[session_id] = []
        return session_id
    
    def add_message(self, session_id: str, role: str, content: str, metadata: Dict[str, Any] = None):
        """
        Add message to conversation history.
        
        Args:
            session_id: Session identifier
            role: 'user' or 'assistant'
            content: Message content
            metadata: Additional metadata (agent used, sources, etc.)
        """
        if session_id not in self.sessions:
            self.create_session(session_id)
        
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        self.sessions[session_id].append(message)
    
    def get_history(self, session_id: str, limit: int = None) -> List[Dict[str, Any]]:
        """
        Retrieve conversation history.
        
        Args:
            session_id: Session identifier
            limit: Maximum number of recent messages to return
            
        Returns:
            List of conversation messages
        """
        if session_id not in self.sessions:
            return []
        
        history = self.sessions[session_id]
        
        if limit:
            return history[-limit:]
        return history
    
    def clear_session(self, session_id: str):
        """Clear conversation history for session"""
        if session_id in self.sessions:
            self.sessions[session_id] = []
