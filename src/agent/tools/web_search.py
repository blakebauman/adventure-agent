"""Web search tools using Tavily."""

from __future__ import annotations

from typing import Any, Dict, List

from langchain_community.tools.tavily_search import TavilySearchResults


class WebSearchTool:
    """Web search tool using Tavily."""

    def __init__(self, api_key: str | None = None):
        """Initialize web search tool."""
        if api_key:
            self.search = TavilySearchResults(
                max_results=5, tavily_api_key=api_key
            )
        else:
            self.search = None

    def search_web(self, query: str) -> List[Dict[str, Any]]:
        """Search the web for information."""
        if not self.search:
            # Fallback: return empty results if no API key
            return []
        try:
            results = self.search.invoke({"query": query})
            return results if isinstance(results, list) else []
        except Exception as e:
            print(f"Web search error: {e}")
            return []

