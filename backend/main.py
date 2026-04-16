from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import upload, query
from config import settings

# Initialize FastAPI app
app = FastAPI(
    title="AI Project Intelligence Assistant",
    description="RAG-based system for document Q&A and data analysis",
    version="1.0.0"
)

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router, prefix="/api", tags=["Upload"])
app.include_router(query.router, prefix="/api", tags=["Query"])

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "message": "AI Project Intelligence Assistant API",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "google_api_configured": bool(settings.google_api_key),
        "chroma_dir": settings.chroma_persist_dir,
        "upload_dir": settings.upload_dir
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
