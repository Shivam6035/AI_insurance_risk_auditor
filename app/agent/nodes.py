

import json
import re
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, ToolMessage
from app.core.config import settings
from app.models.response import AuditResponse
from app.agent.tools import search_policy_guidelines
from app.agent.prompts import SYSTEM_PROMPT

# Standard production model with retries and timeout safety
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=settings.GOOGLE_API_KEY,
    temperature=0.1,
    max_retries=3,
    timeout=45
)

# Bind search tool
available_tools = [search_policy_guidelines]
llm_with_tools = llm.bind_tools(available_tools)

# Bind structured output for direct Pydantic extraction
structured_llm = llm.with_structured_output(AuditResponse)


def clean_json_string(content: str) -> str:
    """Robust extraction of pure JSON ignoring markdown fences and conversational noise."""
    if not content or not content.strip():
        raise ValueError("LLM returned an empty response string.")

    # 1. Search for an explicit fenced block first
    pattern = r"```(?:json)?\s*([\s\S]*?)\s*```"
    match = re.search(pattern, content)
    if match:
        return match.group(1).strip()

    # 2. Extract first outer JSON object if fences are missing
    start_brace = content.find("{")
    end_brace = content.rfind("}")
    if start_brace != -1 and end_brace != -1 and end_brace > start_brace:
        return content[start_brace : end_brace + 1].strip()

    return content.strip()


def call_llm(state: dict) -> dict:
    """The Reasoning Node: Invokes tools or prepares final structured output."""
    messages = state.get("messages", [])
    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages

    response = llm_with_tools.invoke(messages)

    # If the LLM didn't request a tool, validate and enforce structured JSON
    if not getattr(response, "tool_calls", None):
        try:
            # Enforce clean payload if content string needs normalization
            cleaned = clean_json_string(str(response.content))
            parsed = json.loads(cleaned)
            # Re-serialize clean string so downstream parsers get valid JSON
            response.content = json.dumps(parsed)
        except Exception:
            # Fallback directly through structured LLM schema
            structured_res = structured_llm.invoke(messages)
            response.content = structured_res.model_dump_json()

    return {"messages": [response]}


def execute_search_tools(state: dict) -> dict:
    """The Action Node: Runs Tavily and feeds results back to Gemini."""
    messages = state.get("messages", [])
    last_message = messages[-1]
    tool_outputs = []

    for tool_call in getattr(last_message, "tool_calls", []):
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