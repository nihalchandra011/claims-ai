# backend/web_search.py
import os
import requests

OLLAMA_SEARCH_URL = "https://ollama.com/api/web_search"

def ollama_web_search(query: str, max_results: int = 5) -> str:
    """
    Query the web via Ollama's web search API.
    This returns concatenated result snippets.
    Requires a valid OLLAMA_API_KEY in environment variables.
    """
    api_key = os.getenv("OLLAMA_API_KEY")
    if not api_key:
        raise RuntimeError("OLLAMA_API_KEY not set")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {"query": query, "max_results": max_results}
    
    r = requests.post(OLLAMA_SEARCH_URL, json=payload, headers=headers, timeout=10)
    r.raise_for_status()
    data = r.json()
    
    # Ollama returns something like: {"results":[{"title":"...", "snippet":"..."}]}
    results = data.get("results") or []
    snippets = [r.get("snippet", r.get("title", "")) for r in results]
    
    return "\n".join(snippets)