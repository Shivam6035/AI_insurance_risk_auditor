# from pydantic import BaseModel, Field

# class AuditRequest(BaseModel):
#     # The frontend simply passes the natural language request from the user
#     user_query: str = Field(
#         ..., 
#         example="Audit my HDFC ERGO Optima Secure policy. The base sum insured is 10 Lakhs."
#     )

# app/models/request.py
from pydantic import BaseModel, Field

class AuditRequest(BaseModel):
    user_query: str = Field(
        ...,
        description="The user's policy inquiry or audit request.",
        json_schema_extra={"example": "Audit my HDFC ERGO Optima Secure policy with 10L cover."}
    )