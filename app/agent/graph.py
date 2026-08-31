from langgraph.graph import StateGraph, START, END
from app.agent.state import AgentState
from app.agent.nodes import call_llm, execute_search_tools
from langchain_tavily import TavilySearch

# 1. Initialize the Graph with the State schema
# AgentState is a TypedDict (defined in state.py) that holds the conversation history,
# the extracted provider details, and the final scored output.
workflow = StateGraph(AgentState)

# 2. Add Nodes
# Nodes are the actual Python functions that do the work.
workflow.add_node("reasoning_agent", call_llm)
workflow.add_node("web_search_tools", execute_search_tools)

# 3. Define the Conditional Edge Logic
def should_continue(state: AgentState) -> str:
    """
    Evaluates the LLM's latest response to determine the next step in the graph.
    """
    last_message = state["messages"][-1]
    
    # If the LLM requests data it doesn't have, it generates a 'tool_call'
    if last_message.tool_calls:
        return "search"
    
    # If no tools are called, the LLM has enough information to score the policy
    return "finish"

# 4. Wire the Graph Together
# Start by passing the user's input directly to the LLM
workflow.add_edge(START, "reasoning_agent")

# Add the decision point after the LLM thinks
workflow.add_conditional_edges(
    "reasoning_agent",
    should_continue,
    {
        "search": "web_search_tools",  # Route to the search tools
        "finish": END                  # Exit the loop and return the score
    }
)

# 5. Create the Feedback Loop
# After the tool fetches web data, it MUST go back to the LLM for evaluation
workflow.add_edge("web_search_tools", "reasoning_agent")

# 6. Compile the Graph
# This creates a runnable LangChain object that tracks state automatically
auditor_agent = workflow.compile()

import asyncio
from typing import TypedDict
from langchain_community.tools.tavily_search import TavilySearchResults
from app.agent.prompts import COMPARE_SYSTEM_PROMPT
from app.models.response import CompareResponse
from app.agent.nodes import llm # Reusing your existing LLM instance

class CompareState(TypedDict):
    policy_a_query: str
    policy_b_query: str
    policy_a_context: str
    policy_b_context: str
    final_result: str

search_tool = TavilySearch(max_results=5, search_depth="advanced", include_raw_content="text")

async def fetch_contexts(state: CompareState):
    query_a = state["policy_a_query"]
    query_b = state["policy_b_query"]
    
    result_a, result_b = await asyncio.gather(
        search_tool.ainvoke({"query": f"{query_a} health insurance policy wordings clauses limits"}),
        search_tool.ainvoke({"query": f"{query_b} health insurance policy wordings clauses limits"})
    )
    return {"policy_a_context": str(result_a), "policy_b_context": str(result_b)}

async def generate_comparison(state: CompareState):
    sys_msg = COMPARE_SYSTEM_PROMPT
    user_msg = (
        f"POLICY A ({state['policy_a_query']}):\n{state['policy_a_context']}\n\n"
        f"POLICY B ({state['policy_b_query']}):\n{state['policy_b_context']}"
    )
    
    structured_llm = llm.with_structured_output(CompareResponse)
    response = await structured_llm.ainvoke([
        {"role": "system", "content": sys_msg},
        {"role": "user", "content": user_msg}
    ])
    return {"final_result": response.model_dump_json()}

compare_builder = StateGraph(CompareState)
compare_builder.add_node("search", fetch_contexts)
compare_builder.add_node("compare", generate_comparison)
compare_builder.add_edge(START, "search")
compare_builder.add_edge("search", "compare")
compare_builder.add_edge("compare", END)

compare_graph = compare_builder.compile()


import asyncio
from langgraph.graph import START, END
from app.agent.prompts import COMPARE_SYSTEM_PROMPT
from app.models.response import CompareResponse
# Reusing your existing `llm` and `search_tool` (TavilySearch) defined earlier in this file

class CompareState(TypedDict):
    policy_a_query: str
    policy_b_query: str
    policy_a_context: str
    policy_b_context: str
    final_result: str

async def fetch_contexts_parallel(state: CompareState):
    """Fires two Tavily web searches concurrently to save time."""
    query_a = state["policy_a_query"]
    query_b = state["policy_b_query"]
    
    result_a, result_b = await asyncio.gather(
        search_tool.ainvoke({"query": f"{query_a} health insurance policy wordings clauses"}),
        search_tool.ainvoke({"query": f"{query_b} health insurance policy wordings clauses"})
    )
    return {"policy_a_context": str(result_a), "policy_b_context": str(result_b)}

async def generate_comparison(state: CompareState):
    """Evaluates both policies and outputs structured JSON for the frontend charts."""
    user_msg = (
        f"POLICY A ({state['policy_a_query']}):\n{state['policy_a_context']}\n\n"
        f"POLICY B ({state['policy_b_query']}):\n{state['policy_b_context']}"
    )
    
    # Enforce strict JSON output using our new Pydantic schema
    structured_llm = llm.with_structured_output(CompareResponse)
    response = await structured_llm.ainvoke([
        {"role": "system", "content": COMPARE_SYSTEM_PROMPT},
        {"role": "user", "content": user_msg}
    ])
    
    return {"final_result": response.model_dump_json()}

# Compile the secondary Comparison Graph
compare_builder = StateGraph(CompareState)
compare_builder.add_node("search", fetch_contexts_parallel)
compare_builder.add_node("compare", generate_comparison)
compare_builder.add_edge(START, "search")
compare_builder.add_edge("search", "compare")
compare_builder.add_edge("compare", END)

compare_graph = compare_builder.compile()