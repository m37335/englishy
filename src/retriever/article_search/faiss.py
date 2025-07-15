"""
FAISS-based vector search for English learning content.
"""

import numpy as np
import faiss
from typing import List, Dict, Any, Optional
import pickle
import os
from pathlib import Path

from retriever.search_result import SearchResult, SearchQuery, SearchResults
from src.utils.logging import logger


class FAISSSearch:
    """FAISS-based vector search for English learning content."""
    
    def __init__(self, index_path: str = None, dimension: int = 1536):
        self.index_path = index_path
        self.dimension = dimension
        self.index = None
        self.chunks = []
        self.is_loaded = False
        
    def build_index(self, chunks: List[Dict[str, Any]], embeddings: List[List[float]]):
        """Build FAISS index from chunks and embeddings."""
        if not chunks or not embeddings:
            logger.warning("No chunks or embeddings provided for index building")
            return
        
        # Convert embeddings to numpy array
        embeddings_array = np.array(embeddings, dtype=np.float32)
        
        # Create FAISS index
        self.index = faiss.IndexFlatIP(self.dimension)  # Inner product for cosine similarity
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings_array)
        
        # Add vectors to index
        self.index.add(embeddings_array)
        
        # Store chunks
        self.chunks = chunks
        
        logger.info(f"Built FAISS index with {len(chunks)} chunks and {self.dimension} dimensions")
        
        # Save index if path is provided
        if self.index_path:
            self.save_index()
    
    def search(self, query_embedding: List[float], k: int = 10) -> SearchResults:
        """Search for similar chunks using query embedding."""
        if not self.index or not self.chunks:
            logger.warning("Index not built or chunks not loaded")
            return SearchResults()
        
        # Convert query embedding to numpy array
        query_array = np.array([query_embedding], dtype=np.float32)
        
        # Normalize query embedding
        faiss.normalize_L2(query_array)
        
        # Search
        scores, indices = self.index.search(query_array, k)
        
        # Create search results
        results = SearchResults()
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.chunks):
                chunk = self.chunks[idx]
                result = SearchResult(
                    id=chunk.get('id', f'chunk_{idx}'),
                    type=chunk.get('type', 'unknown'),
                    content=chunk.get('content', {}),
                    text=chunk.get('text', ''),
                    score=float(score),
                    metadata=chunk.get('metadata', {})
                )
                results.add_result(result)
        
        logger.info(f"Found {len(results.results)} results for query")
        return results
    
    def search_by_text(self, query_text: str, encoder, k: int = 10) -> SearchResults:
        """Search by text using encoder."""
        # Encode query text
        query_embedding = encoder.encode_single_text(query_text)
        
        if not query_embedding:
            logger.warning("Failed to encode query text")
            return SearchResults()
        
        return self.search(query_embedding, k)
    
    def save_index(self):
        """Save FAISS index and chunks to disk."""
        if not self.index_path:
            logger.warning("No index path provided for saving")
            return
        
        try:
            # Create directory if it doesn't exist
            Path(self.index_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Save FAISS index
            faiss.write_index(self.index, f"{self.index_path}.faiss")
            
            # Save chunks
            with open(f"{self.index_path}.chunks", 'wb') as f:
                pickle.dump(self.chunks, f)
            
            logger.info(f"Saved index to {self.index_path}")
            
        except Exception as e:
            logger.error(f"Error saving index: {e}")
            raise
    
    def load_index(self):
        """Load FAISS index and chunks from disk."""
        if not self.index_path:
            logger.warning("No index path provided for loading")
            return
        
        try:
            # Load FAISS index
            index_file = f"{self.index_path}.faiss"
            if os.path.exists(index_file):
                self.index = faiss.read_index(index_file)
            else:
                logger.warning(f"Index file not found: {index_file}")
                return
            
            # Load chunks
            chunks_file = f"{self.index_path}.chunks"
            if os.path.exists(chunks_file):
                with open(chunks_file, 'rb') as f:
                    self.chunks = pickle.load(f)
            else:
                logger.warning(f"Chunks file not found: {chunks_file}")
                return
            
            self.is_loaded = True
            logger.info(f"Loaded index with {len(self.chunks)} chunks")
            
        except Exception as e:
            logger.error(f"Error loading index: {e}")
            raise
    
    def get_index_info(self) -> Dict[str, Any]:
        """Get information about the index."""
        if not self.index:
            return {"status": "not_built"}
        
        return {
            "status": "built" if self.is_loaded else "loaded",
            "total_chunks": len(self.chunks),
            "dimension": self.dimension,
            "index_type": "FlatIP"
        } 