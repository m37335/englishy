"""
Search result data structures for English learning content.
"""

from dataclasses import dataclass
from typing import Dict, Any, List, Optional


@dataclass
class SearchResult:
    """Represents a search result."""
    id: str
    type: str
    content: Dict[str, Any]
    text: str
    score: float
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'type': self.type,
            'content': self.content,
            'text': self.text,
            'score': self.score,
            'metadata': self.metadata
        }


@dataclass
class SearchQuery:
    """Represents a search query."""
    text: str
    filters: Optional[Dict[str, Any]] = None
    limit: int = 10
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'text': self.text,
            'filters': self.filters,
            'limit': self.limit
        }


class SearchResults:
    """Container for search results."""
    
    def __init__(self, results: List[SearchResult] = None):
        self.results = results or []
    
    def add_result(self, result: SearchResult):
        """Add a search result."""
        self.results.append(result)
    
    def get_top_results(self, limit: int = None) -> List[SearchResult]:
        """Get top results sorted by score."""
        sorted_results = sorted(self.results, key=lambda x: x.score, reverse=True)
        if limit:
            return sorted_results[:limit]
        return sorted_results
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'results': [result.to_dict() for result in self.results],
            'total_count': len(self.results)
        } 