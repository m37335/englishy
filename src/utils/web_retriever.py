"""
Web retriever utilities for Englishy.
"""

def load_web_retriever(name: str):
    """
    Load a web retriever by name.
    
    Args:
        name: Name of the web search engine
        
    Returns:
        Web retriever instance
    """
    name_lower = name.lower()
    if name_lower == "duckduckgo":
        from src.retriever.web_search.duckduckgo_search import DuckDuckGoSearchWebRetriever
        return DuckDuckGoSearchWebRetriever()
    else:
        raise ValueError(f"Unsupported web search engine: {name}") 