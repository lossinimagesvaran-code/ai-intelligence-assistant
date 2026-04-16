from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter

class TextChunker:
    """
    Splits text into smaller chunks for embedding and retrieval.
    Uses recursive splitting to maintain semantic coherence.
    """
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        """
        Initialize text splitter with specified chunk parameters.
        
        Args:
            chunk_size: Maximum characters per chunk
            chunk_overlap: Number of overlapping characters between chunks
        """
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def split_text(self, text: str) -> List[str]:
        """
        Split text into chunks.
        
        Args:
            text: Input text to split
            
        Returns:
            List of text chunks
        """
        return self.splitter.split_text(text)
