import os
from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults

# 1. Initialize the underlying Tavily API wrapper
# We limit max_results to 3 to avoid overflowing the LLM's context window, 
# but request the "advanced" depth to get the raw HTML/text of the target pages.
tavily_search = TavilySearchResults(
    max_results=3,
    search_depth="advanced",
    include_raw_content=True
)

# 2. Define the tool using the @tool decorator
# The docstring below is NOT just for developers - the LLM actively reads it 
# to understand the tool's purpose and how to format its input.
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
        # Execute the search query via Tavily
        results = tavily_search.invoke({"query": query})
        
        if not results:
            return "No results found. Try a different search query or use fewer keywords."

        # 3. Format the JSON response into a clean string for the LLM
        formatted_results = []
        for doc in results:
            source_url = doc.get("url", "Unknown URL")
            
            # Prefer raw_content if available, as it contains the full page text 
            # where the deep clauses usually live. Fallback to the snippet content.
            page_text = doc.get("raw_content") or doc.get("content", "No content extracted.")
            
            # Truncate extremely long pages to prevent context window bloat
            # 10,000 characters is roughly 2,500 tokens.
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