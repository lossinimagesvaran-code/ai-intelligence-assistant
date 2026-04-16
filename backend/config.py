import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    Uses pydantic for validation and type safety.
    """
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")
    chroma_persist_dir: str = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
    upload_dir: str = os.getenv("UPLOAD_DIR", "./uploads")
    
    # RAG Configuration
    chunk_size: int = 500
    chunk_overlap: int = 50
    
    # LLM Configuration
    model_name: str = "gemini-2.5-flash"
    temperature: float = 0.7
    
    class Config:
        env_file = ".env"

settings = Settings()

# Ensure directories exist
os.makedirs(settings.chroma_persist_dir, exist_ok=True)
os.makedirs(settings.upload_dir, exist_ok=True)
