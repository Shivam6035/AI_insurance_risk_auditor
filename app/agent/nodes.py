import json
import re

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


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

def clean_json_string(content: str) -> str:
    """Removes markdown code fences and cleans whitespace."""
    if not content:
        raise ValueError("LLM returned an empty response.")
    
    # Strip markdown code blocks like ```json ... ``` or ``` ... ```
    cleaned = re.sub(r"^```(?:json)?\s*", "", content.strip(), flags=re.MULTILINE)
    cleaned = re.sub(r"\s*```$", "", cleaned.strip(), flags=re.MULTILINE)
    return cleaned.strip()

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