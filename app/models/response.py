from pydantic import BaseModel
from typing import List

class Deduction(BaseModel):
    category: str
    penalty: int
    reason: str
    source_url: str

class AuditResponse(BaseModel):
    policy_name: str
    provider: str
    base_score: int
    final_score: int
    deductions: List[Deduction]
    verdict: str