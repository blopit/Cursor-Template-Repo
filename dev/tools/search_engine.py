"""Search engine integration module."""
from typing import List, Dict, Any, Optional
from duckduckgo_search import DDGS

def search(
    query: str,
    max_results: int = 10,
    region: str = "wt-wt",
    safesearch: str = "moderate",
    **kwargs: Any
) -> List[Dict[str, str]]:
    """Search the web using DuckDuckGo."""
    with DDGS() as ddgs:
        results = list(ddgs.text(
            query,
            region=region,
            safesearch=safesearch,
            max_results=max_results
        ))
    
    # Format results
    formatted_results = []
    for result in results:
        formatted_results.append({
            "title": result["title"],
            "link": result["link"],
            "snippet": result["body"]
        })
    
    return formatted_results

def search_news(
    query: str,
    max_results: int = 10,
    region: str = "wt-wt",
    **kwargs: Any
) -> List[Dict[str, str]]:
    """Search news articles using DuckDuckGo."""
    with DDGS() as ddgs:
        results = list(ddgs.news(
            query,
            region=region,
            max_results=max_results
        ))
    
    # Format results
    formatted_results = []
    for result in results:
        formatted_results.append({
            "title": result["title"],
            "link": result["link"],
            "snippet": result["body"],
            "date": result.get("date", ""),
            "source": result.get("source", "")
        })
    
    return formatted_results

def search_images(
    query: str,
    max_results: int = 10,
    size: Optional[str] = None,
    color: Optional[str] = None,
    type_image: Optional[str] = None,
    layout: Optional[str] = None,
    **kwargs: Any
) -> List[Dict[str, str]]:
    """Search images using DuckDuckGo."""
    with DDGS() as ddgs:
        results = list(ddgs.images(
            query,
            max_results=max_results,
            size=size,
            color=color,
            type_image=type_image,
            layout=layout
        ))
    
    # Format results
    formatted_results = []
    for result in results:
        formatted_results.append({
            "title": result["title"],
            "image": result["image"],
            "thumbnail": result.get("thumbnail", ""),
            "source": result["source"],
            "width": result.get("width", ""),
            "height": result.get("height", "")
        })
    
    return formatted_results 