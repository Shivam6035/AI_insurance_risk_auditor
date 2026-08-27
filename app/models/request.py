from pydantic import BaseModel, Field

class AuditRequest(BaseModel):
    # The frontend simply passes the natural language request from the user
    user_query: str = Field(
        ..., 
        example="Audit my HDFC ERGO Optima Secure policy. The base sum insured is 10 Lakhs."
    )