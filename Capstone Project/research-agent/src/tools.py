import logging
import requests

logger = logging.getLogger("agent")

def web_search(query: str) -> list:
    """
    Mock search tool. Replace with real API (Bing, Tavily, SerpAPI)
    """
    logger.info(f"Tool Call: web_search('{query}')")

    # Mock search results
    results = [
        {"title": f"About {query}", "content": f"This is research data about {query}."},
        {"title": f"{query} Overview", "content": f"Detailed overview and analysis of {query}."},
    ]
    
    logger.info(f"Tool Result: {len(results)} items")
    return results
