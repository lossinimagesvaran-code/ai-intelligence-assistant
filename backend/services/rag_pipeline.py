from typing import List, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from services.vector_store import VectorStoreService
from utils.text_splitter import TextChunker
from config import settings

class RAGPipeline:
    """
    Retrieval-Augmented Generation pipeline.
    Orchestrates document chunking, embedding, retrieval, and answer generation.
    """
    
    def __init__(self):
        """Initialize RAG components"""
        self.vector_store = VectorStoreService()
        self.text_chunker = TextChunker(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap
        )
        self.llm = ChatGoogleGenerativeAI(
            model=f"models/{settings.model_name}",
            temperature=settings.temperature,
            google_api_key=settings.google_api_key
        )
    
    def index_document(self, text: str, filename: str):
        """
        Process and index a document into vector store.
        
        Args:
            text: Full document text
            filename: Source filename for metadata
        """
        # Split text into chunks
        chunks = self.text_chunker.split_text(text)
        
        # Create metadata for each chunk
        metadata = [
            {"source": filename, "chunk_id": i}
            for i in range(len(chunks))
        ]
        
        # Add to vector store
        self.vector_store.add_documents(chunks, metadata)
    
    def query(self, question: str) -> Dict[str, Any]:
        """
        Answer question using RAG.
        
        Args:
            question: User question
            
        Returns:
            Dict with answer and source citations
        """
        # Retrieve relevant chunks
        relevant_docs = self.vector_store.similarity_search(question, k=4)
        
        if not relevant_docs:
            return {
                "answer": "I don't have enough information to answer this question.",
                "sources": []
            }
        
        # Build context from retrieved chunks
        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        
        # Create prompt
        prompt_template = """Use the following context to answer the question. 
If you cannot answer based on the context, say so.

Context:
{context}

Question: {question}

Answer:"""
        
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        # Generate answer
        formatted_prompt = prompt.format(context=context, question=question)
        answer = self.llm.invoke(formatted_prompt).content
        
        # Extract source information
        sources = []
        for doc in relevant_docs:
            sources.append({
                "source": doc.metadata.get("source", "Unknown"),
                "chunk_id": doc.metadata.get("chunk_id", 0),
                "content": doc.page_content[:200] + "..."  # Preview
            })
        
        return {
            "answer": answer,
            "sources": sources
        }
