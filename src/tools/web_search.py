from tavily import TavilyClient
from typing import Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

class MedicalWebSearchTool:
    def __init__(self):
        """Initialize the web search tool with Tavily API"""
        self.client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    
    def search(self, query: str) -> Dict[str, Any]:
        """
        Perform a web search for medical information.
        
        Args:
            query (str): The search query
            
        Returns:
            Dict[str, Any]: Search results
        """
        try:
            response = self.client.search(
                query=f"medical information about {query}",
                search_depth="advanced",
                max_results=5
            )
            return response
        except Exception as e:
            return {"error": str(e)}
