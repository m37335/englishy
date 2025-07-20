"""
DuckDuckGo search for English learning content.
"""

import requests
from typing import List, Dict, Any, Optional
import logging
from duckduckgo_search import DDGS

logger = logging.getLogger(__name__)

class DuckDuckGoSearchWebRetriever:
    """DuckDuckGo search engine for English learning resources."""
    
    def __init__(self, search_engine: str = "duckduckgo"):
        """Initialize the search engine."""
        self.search_engine = search_engine
        self.ddgs = DDGS() if search_engine == "duckduckgo" else None
    
    def search(self, query: str, k: int = 10, domains: List[str] = None) -> List[Dict[str, Any]]:
        """
        Search for English learning resources.
        
        Args:
            query: Search query
            k: Maximum number of results to return
            domains: Optional list of domains to search
        
        Returns:
            List of search results
        """
        try:
            if self.search_engine == "duckduckgo":
                return self._search_duckduckgo(query, k, domains)
            else:
                logger.warning(f"Unsupported search engine: {self.search_engine}")
                return []
                
        except Exception as e:
            logger.error(f"Error in search: {e}")
            return []
    
    def _search_duckduckgo(self, query: str, k: int, domains: List[str] = None) -> List[Dict[str, Any]]:
        """Search using DuckDuckGo."""
        try:
            # Add English learning context to the query
            enhanced_query = f"English learning {query} grammar vocabulary pronunciation"
            
            # Add domain restrictions if specified
            if domains:
                domain_query = " OR ".join([f"site:{domain}" for domain in domains])
                enhanced_query = f"{enhanced_query} {domain_query}"
            
            logger.info(f"DuckDuckGo search: query='{query}', enhanced_query='{enhanced_query}', k={k}")
            
            results = []
            search_results = self.ddgs.text(enhanced_query, max_results=k)
            
            logger.info(f"DuckDuckGo raw results count: {len(list(search_results)) if search_results else 0}")
            
            # Convert generator to list and process
            search_results_list = list(search_results) if search_results else []
            logger.info(f"DuckDuckGo search_results_list length: {len(search_results_list)}")
            
            for i, result in enumerate(search_results_list):
                # Debug: Print the entire result structure
                logger.info(f"Processing result {i+1}: Full result structure: {result}")
                
                # Try different possible URL field names
                url = result.get('link') or result.get('url') or result.get('href') or result.get('url_link')
                title = result.get('title') or result.get('name') or 'No title'
                snippet = result.get('body') or result.get('snippet') or result.get('description') or ''
                
                logger.info(f"Processing result {i+1}: title='{title}', url='{url}'")
                
                results.append({
                    "title": title,
                    "url": url,
                    "snippet": snippet,
                    "source": "duckduckgo"
                })
            
            logger.info(f"DuckDuckGo final results count: {len(results)}")
            return results[:k]
            
        except Exception as e:
            logger.error(f"Error in DuckDuckGo search: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return []
    
    def search_grammar_rules(self, topic: str) -> List[Dict[str, Any]]:
        """
        Search for specific English grammar rules.
        
        Args:
            topic: Grammar topic (e.g., "present perfect", "conditionals")
        
        Returns:
            List of grammar resources
        """
        query = f"English grammar rules {topic} examples exercises"
        return self.search(query, k=5)
    
    def search_vocabulary(self, topic: str) -> List[Dict[str, Any]]:
        """
        Search for vocabulary resources.
        
        Args:
            topic: Vocabulary topic (e.g., "business English", "travel vocabulary")
        
        Returns:
            List of vocabulary resources
        """
        query = f"English vocabulary {topic} words phrases"
        return self.search(query, k=5)
    
    def search_pronunciation(self, topic: str) -> List[Dict[str, Any]]:
        """
        Search for pronunciation resources.
        
        Args:
            topic: Pronunciation topic (e.g., "th sound", "intonation")
        
        Returns:
            List of pronunciation resources
        """
        query = f"English pronunciation {topic} audio practice"
        return self.search(query, k=5)
    
    def search_practice_exercises(self, topic: str) -> List[Dict[str, Any]]:
        """
        Search for practice exercises.
        
        Args:
            topic: Exercise topic
        
        Returns:
            List of exercise resources
        """
        query = f"English practice exercises {topic} worksheets"
        return self.search(query, k=5)

# For backward compatibility
DuckDuckGoSearch = DuckDuckGoSearchWebRetriever 