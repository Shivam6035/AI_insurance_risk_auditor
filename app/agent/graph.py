from langgraph.graph import StateGraph, START, END
from app.agent.state import AgentState
from app.agent.nodes import call_llm, execute_search_tools

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