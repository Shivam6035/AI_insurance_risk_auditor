import os
from dotenv import load_dotenv, find_dotenv

# 1. Force Python to find and load the .env file into os.environ
load_dotenv(find_dotenv())

from langchain_core.tools import tool
# Import the new class name from the new package
from langchain_tavily import TavilySearch


# 2. Initialize the updated Tavily tool
tavily_search = TavilySearch(
    max_results=3,
    search_depth="advanced",
    # The new package prefers "text" or "markdown" instead of True
    include_raw_content="text" 
)

@tool
def search_policy_guidelines(query: str) -> str:
    """
    Use this tool to search the web for official insurance policy guidelines, 
    brochures, waiting periods, and customer information sheets. 
    
    CRITICAL: Always try to restrict your search to the official provider domain.
    Example input: 'site:hdfcergo.com Optima Secure room rent limit'
    Example input: 'site:starhealth.in Comprehensive Insurance PED waiting period'
    """
    
    print(f"--> [Tavily] Executing web search for: {query}")
    
    try:
        # Execute the search query
        response = tavily_search.invoke({"query": query})
        
        # In the new package, the actual docs are nested under the "results" key
        results = response.get("results", [])
        
        if not results:
            return "No results found. Try a different search query or use fewer keywords."

        formatted_results = []
        for doc in results:
            source_url = doc.get("url", "Unknown URL")
            
            # Prefer raw_content if available, as it contains the full page text 
            page_text = doc.get("raw_content") or doc.get("content", "No content extracted.")
            
            # Truncate extremely long pages to prevent context window bloat
            if len(page_text) > 10000:
                page_text = page_text[:10000] + "... [Content Truncated]"
                
            formatted_results.append(
                f"Source URL: {source_url}\n"
                f"Extracted Text:\n{page_text}\n"
                f"{'-' * 60}"
            )
            
        return "\n".join(formatted_results)
        
    except Exception as e:
        return f"Web search failed with error: {str(e)}. Please modify the query and try again."