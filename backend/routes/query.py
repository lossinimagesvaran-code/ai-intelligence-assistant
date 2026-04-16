from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from agents.router_agent import RouterAgent
from services.conversation_manager import ConversationManager
from routes.upload import get_agents, get_uploaded_files

router = APIRouter()

# Initialize conversation manager
conversation_manager = ConversationManager()

# Default session for simplicity (in production, use user-specific sessions)
DEFAULT_SESSION = "default_session"
conversation_manager.create_session(DEFAULT_SESSION)

class QueryRequest(BaseModel):
    """Request model for query endpoint"""
    question: str
    session_id: Optional[str] = DEFAULT_SESSION

class QueryResponse(BaseModel):
    """Response model for query endpoint"""
    answer: str
    agent_used: str
    agent_type: str
    sources: Optional[List[Dict[str, Any]]] = None
    analysis: Optional[Dict[str, Any]] = None
    conversation_history: List[Dict[str, Any]]

@router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest) -> QueryResponse:
    """
    Process user query using appropriate agent.
    
    Args:
        request: Query request with question and optional session_id
        
    Returns:
        Answer with agent info and sources/analysis
    """
    try:
        question = request.question
        session_id = request.session_id
        
        # Get agents and uploaded files
        doc_agent, data_agent = get_agents()
        uploaded_files = get_uploaded_files()
        
        # Check if any files have been uploaded
        if not uploaded_files['documents'] and not uploaded_files['data']:
            return QueryResponse(
                answer="Please upload some files first before asking questions.",
                agent_used="System",
                agent_type="system",
                conversation_history=conversation_manager.get_history(session_id)
            )
        
        # Route query to appropriate agent
        agent_type = RouterAgent.route(question, uploaded_files)
        
        # Get conversation history for context
        history = conversation_manager.get_history(session_id, limit=5)
        
        # Execute query with appropriate agent
        if agent_type == 'document_qa':
            result = doc_agent.answer(question, history)
        else:  # data_analysis
            result = data_agent.answer(question, history)
        
        # Store in conversation history
        conversation_manager.add_message(
            session_id=session_id,
            role="user",
            content=question
        )
        
        conversation_manager.add_message(
            session_id=session_id,
            role="assistant",
            content=result["answer"],
            metadata={
                "agent": result["agent"],
                "agent_type": result["agent_type"],
                "sources": result.get("sources"),
                "analysis": result.get("analysis")
            }
        )
        
        # Get updated history
        updated_history = conversation_manager.get_history(session_id)
        
        return QueryResponse(
            answer=result["answer"],
            agent_used=result["agent"],
            agent_type=result["agent_type"],
            sources=result.get("sources"),
            analysis=result.get("analysis"),
            conversation_history=updated_history
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@router.get("/history/{session_id}")
async def get_history(session_id: str) -> Dict[str, Any]:
    """
    Retrieve conversation history for a session.
    
    Args:
        session_id: Session identifier
        
    Returns:
        Conversation history
    """
    history = conversation_manager.get_history(session_id)
    return {"session_id": session_id, "history": history}

@router.delete("/history/{session_id}")
async def clear_history(session_id: str) -> Dict[str, str]:
    """
    Clear conversation history for a session.
    
    Args:
        session_id: Session identifier
        
    Returns:
        Success message
    """
    conversation_manager.clear_session(session_id)
    return {"message": f"History cleared for session {session_id}"}
