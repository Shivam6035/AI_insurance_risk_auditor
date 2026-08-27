import pytest
from unittest.mock import patch, MagicMock
from langchain_core.messages import AIMessage, ToolCall
from app.agent.graph import should_continue
from app.agent.nodes import execute_search_tools

def test_should_continue_routes_to_search():
    """
    If the LLM generates a tool call, the conditional edge should route 
    the graph to the 'search' node.
    """
    # Create a mock AIMessage containing a tool call
    mock_tool_call = ToolCall(name="search_policy_guidelines", args={"query": "test"}, id="123")
    mock_message = AIMessage(content="", tool_calls=[mock_tool_call])
    
    state = {"messages": [mock_message]}
    
    # Execute the routing function
    next_node = should_continue(state)
    
    assert next_node == "search", f"Expected 'search', but got {next_node}"

def test_should_continue_routes_to_finish():
    """
    If the LLM outputs a final string with no tool calls, the conditional edge 
    should route the graph to 'finish' (END).
    """
    # Create a mock AIMessage with no tool calls
    mock_message = AIMessage(content='{"final_score": 850}')
    
    state = {"messages": [mock_message]}
    
    next_node = should_continue(state)
    
    assert next_node == "finish", f"Expected 'finish', but got {next_node}"

@patch("app.agent.nodes.search_policy_guidelines")
def test_execute_search_tools_handles_success(mock_tool):
    """
    Tests that the tool execution node correctly extracts tool calls, 
    runs them, and wraps the response in a ToolMessage.
    """
    # Mock the tool's return value
    mock_tool.invoke.return_value = "Mocked web search result regarding room rent."
    
    mock_tool_call = ToolCall(name="search_policy_guidelines", args={"query": "room rent"}, id="call_abc123")
    mock_message = AIMessage(content="", tool_calls=[mock_tool_call])
    
    state = {"messages": [mock_message]}
    
    # Execute the node
    result_state = execute_search_tools(state)
    
    assert "messages" in result_state
    tool_message = result_state["messages"][0]
    
    assert tool_message.name == "search_policy_guidelines"
    assert tool_message.tool_call_id == "call_abc123"
    assert "Mocked web search result" in tool_message.content