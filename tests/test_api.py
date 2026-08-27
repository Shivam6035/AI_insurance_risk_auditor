import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from langchain_core.messages import AIMessage

from app.main import app

# Initialize the synchronous test client
client = TestClient(app)

def test_health_check():
    """Verify the server boots up and the health endpoint is responsive."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "insurance-auditor"}

@patch("app.api.routes.auditor_agent.ainvoke", new_callable=AsyncMock)
def test_audit_endpoint_success(mock_ainvoke):
    """
    Verify that a valid user query returns a formatted 200 JSON response 
    when the agent succeeds.
    """
    # Define a mock JSON string exactly as the LLM would output it
    mock_llm_json = """
    {
      "policy_name": "Optima Secure",
      "provider": "HDFC ERGO",
      "base_score": 900,
      "final_score": 800,
      "deductions": [
        {
          "category": "Room Rent Limit",
          "penalty": -100,
          "reason": "Capped at 1%",
          "source_url": "https://example.com"
        }
      ],
      "verdict": "Solid policy with a minor room rent restriction."
    }
    """
    
    # Mock the final state returned by LangGraph
    mock_ainvoke.return_value = {
        "messages": [AIMessage(content=mock_llm_json)]
    }
    
    # Send the test request
    payload = {"user_query": "Audit my HDFC ERGO Optima policy."}
    response = client.post("/api/v1/audit", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["provider"] == "HDFC ERGO"
    assert data["final_score"] == 800
    assert len(data["deductions"]) == 1

@patch("app.api.routes.auditor_agent.ainvoke", new_callable=AsyncMock)
def test_audit_endpoint_handles_bad_json(mock_ainvoke):
    """
    Verify that if the LLM hallucinates and fails to return valid JSON, 
    the API catches it and returns a 500 error instead of crashing.
    """
    # The LLM outputs conversational text instead of JSON
    mock_ainvoke.return_value = {
        "messages": [AIMessage(content="I'm sorry, I couldn't find that policy.")]
    }
    
    payload = {"user_query": "Audit my fake policy."}
    response = client.post("/api/v1/audit", json=payload)
    
    # The route should catch the JSONDecodeError and raise an HTTPException (500)
    assert response.status_code == 500
    assert "valid JSON" in response.json()["detail"]