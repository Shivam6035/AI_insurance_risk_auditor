from typing import TypedDict, Annotated, Optional
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """
    The state dictionary that gets passed between all nodes in the graph.
    """
    
    # The 'messages' key is critical. 
    # By using Annotated with add_messages, LangGraph knows to APPEND new 
    # messages to the list rather than overwriting the entire list.
    # This preserves the conversation history and tool execution logs.
    messages: Annotated[list[BaseMessage], add_messages]
    
    # We store extracted metadata explicitly so the API layer can easily 
    # read them without having to parse through the raw message history.
    policy_name: Optional[str]
    provider: Optional[str]
    
    # Once the agent completes its audit, it will drop the final JSON string here.
    final_score_json: Optional[str]