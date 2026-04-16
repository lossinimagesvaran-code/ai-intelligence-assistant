from typing import List, Dict, Any
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document
from config import settings

class VectorStoreService:
    """
    Manages vector database operations using Chroma.
    Handles document embedding, storage, and similarity search.
    """
    
    def __init__(self):
        """Initialize embeddings model and vector store"""
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=settings.google_api_key,
            task_type="retrieval_document"
        )
        self.vector_store = None
        self._initialize_vector_store()
    
    def _initialize_vector_store(self):
        """Load or create persistent Chroma vector store"""
        try:
            self.vector_store = Chroma(
                persist_directory=settings.chroma_persist_dir,
                embedding_function=self.embeddings
            )
        except Exception as e:
            print(f"Error initializing vector store: {e}")
            self.vector_store = Chroma(
                persist_directory=settings.chroma_persist_dir,
                embedding_function=self.embeddings
            )
    
    def add_documents(self, texts: List[str], metadata: List[Dict[str, Any]]):
        """
        Add text chunks to vector store with metadata.
        
        Args:
            texts: List of text chunks to embed
            metadata: List of metadata dicts (one per text chunk)
        """
        documents = [
            Document(page_content=text, metadata=meta)
            for text, meta in zip(texts, metadata)
        ]
        
        self.vector_store.add_documents(documents)
        self.vector_store.persist()
    
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """
        Search for most similar documents to query.
        
        Args:
            query: User question
            k: Number of results to return
            
        Returns:
            List of most relevant document chunks
        """
        return self.vector_store.similarity_search(query, k=k)
    
    def clear_collection(self):
        """Clear all documents from vector store"""
        try:
            self.vector_store.delete_collection()
            self._initialize_vector_store()
        except Exception as e:
            print(f"Error clearing collection: {e}")
