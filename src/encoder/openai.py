"""
OpenAI embedding encoder for English learning content.
"""

import os
from typing import List, Dict, Any
import numpy as np
from openai import OpenAI

from utils.logging import logger


class OpenAIEncoder:
    """OpenAI embedding encoder for English learning content."""
    
    def __init__(self, model: str = "text-embedding-3-small", api_key: str = None):
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        self.client = OpenAI(api_key=self.api_key)
        
    def encode_texts(self, texts: List[str]) -> List[List[float]]:
        """Encode a list of texts to embeddings."""
        if not texts:
            return []
        
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=texts
            )
            
            embeddings = [embedding.embedding for embedding in response.data]
            logger.info(f"Encoded {len(texts)} texts using {self.model}")
            
            return embeddings
            
        except Exception as e:
            logger.error(f"Error encoding texts with OpenAI: {e}")
            raise
    
    def encode_single_text(self, text: str) -> List[float]:
        """Encode a single text to embedding."""
        embeddings = self.encode_texts([text])
        return embeddings[0] if embeddings else []
    
    def encode_chunks(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Encode chunks with their embeddings."""
        texts = [chunk.get('text', '') for chunk in chunks]
        embeddings = self.encode_texts(texts)
        
        # Add embeddings to chunks
        encoded_chunks = []
        for chunk, embedding in zip(chunks, embeddings):
            encoded_chunk = chunk.copy()
            encoded_chunk['embedding'] = embedding
            encoded_chunks.append(encoded_chunk)
        
        return encoded_chunks
    
    def get_embedding_dimension(self) -> int:
        """Get the dimension of embeddings."""
        # Test with a short text to get dimension
        test_embedding = self.encode_single_text("test")
        return len(test_embedding) 