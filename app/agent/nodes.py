# import json
# # from langchain_openai import ChatOpenAI

# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.messages import SystemMessage, ToolMessage
# from app.agent.tools import search_policy_guidelines
# from app.agent.prompts import SYSTEM_PROMPT
# # Add this at the very top of app/agent/nodes.py if not already present
# from dotenv import load_dotenv, find_dotenv
# load_dotenv(find_dotenv())

# # 1. Initialize the reasoning engine
# # We use a temperature of 0 because auditing requires deterministic, factual evaluation.
# llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)


# # 2. Bind the tools to the LLM
# # This translates your Python functions into a JSON schema the LLM understands,
# # allowing it to natively output "tool_calls".
# available_tools = [search_policy_guidelines]
# llm_with_tools = llm.bind_tools(available_tools)

# def call_llm(state: dict) -> dict:
#     """
#     The Reasoning Node.
#     Reads the user input and any gathered web context, then either requests 
#     more data via a search tool or generates the final policy health score.
#     """
#     messages = state.get("messages", [])
    
#     # Inject the system prompt (the instructions and scoring rubric) if not present
#     if not messages or not isinstance(messages[0], SystemMessage):
#         messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
        
#     # The LLM processes the entire conversation history
#     response = llm_with_tools.invoke(messages)
    
#     # LangGraph automatically appends this response to the state's "messages" list
#     return {"messages": [response]}


# def execute_search_tools(state: dict) -> dict:
#     """
#     The Action Node.
#     Extracts the requested search queries from the LLM, executes the web scrape,
#     and formats the data so the LLM can read it on the next loop.
#     """
#     messages = state.get("messages", [])
#     last_message = messages[-1]
    
#     tool_outputs = []
    
#     # The LLM might request multiple searches at once (Parallel Tool Calling)
#     # e.g., searching for "room rent" and "waiting period" simultaneously.
#     for tool_call in last_message.tool_calls:
#         tool_name = tool_call["name"]
#         tool_args = tool_call["args"]
#         tool_call_id = tool_call["id"]
        
#         print(f"--> [Action] Executing tool '{tool_name}' with args: {tool_args}")
        
#         # Route to the correct Python function
#         if tool_name == "search_policy_guidelines":
#             try:
#                 # Execute the actual web search / scraping
#                 result = search_policy_guidelines.invoke(tool_args)
#                 result_str = str(result)
#             except Exception as e:
#                 # Crucial: Catch errors and return them to the LLM so it can 
#                 # self-correct and try a different search query!
#                 result_str = f"Error executing search. Try a different query. Error: {str(e)}"
#         else:
#             result_str = f"Error: Tool '{tool_name}' is not recognized."
            
#         # Wrap the raw string result in a ToolMessage. 
#         # The tool_call_id proves to the LLM that this is the answer to its specific request.
#         tool_outputs.append(
#             ToolMessage(
#                 content=result_str,
#                 tool_call_id=tool_call_id,
#                 name=tool_name
#             )
#         )
        
#     # Return the results to be appended to the state
#     return {"messages": tool_outputs}

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, ToolMessage
from app.core.config import settings
from app.agent.tools import search_policy_guidelines
from app.agent.prompts import SYSTEM_PROMPT

# Initialize Google Gemini 1.5 Flash
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    temperature=0,
    google_api_key=settings.GOOGLE_API_KEY
)

# Bind the search tool directly to Gemini
available_tools = [search_policy_guidelines]
llm_with_tools = llm.bind_tools(available_tools)

def call_llm(state: dict) -> dict:
    """The Reasoning Node."""
    messages = state.get("messages", [])
    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
        
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def execute_search_tools(state: dict) -> dict:
    """The Action Node."""
    messages = state.get("messages", [])
    last_message = messages[-1]
    tool_outputs = []
    
    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        tool_call_id = tool_call["id"]
        
        print(f"--> [Gemini Action] Executing tool '{tool_name}' with args: {tool_args}")
        
        if tool_name == "search_policy_guidelines":
            try:
                result = search_policy_guidelines.invoke(tool_args)
                result_str = str(result)
            except Exception as e:
                result_str = f"Error executing search: {str(e)}"
        else:
            result_str = f"Error: Tool '{tool_name}' is not recognized."
            
        tool_outputs.append(
            ToolMessage(
                content=result_str,
                tool_call_id=tool_call_id,
                name=tool_name
            )
        )
    return {"messages": tool_outputs}