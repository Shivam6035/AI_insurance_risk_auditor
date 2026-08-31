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

from typing import List, Dict
from pydantic import Field

class ChartMetrics(BaseModel):
    labels: List[str] = Field(
        default=["Room Rent", "PED Wait Time", "Co-Pay", "No Claim Bonus", "Daycare Limits"]
    )
    policy_a_scores: List[int]
    policy_b_scores: List[int]

class CompareResponse(BaseModel):
    policy_a_name: str
    policy_b_name: str
    winner: str
    chart_data: ChartMetrics
    executive_summary: str
    detailed_analysis: Dict[str, str]

from typing import List, Dict

class ChartMetrics(BaseModel):
    labels: List[str] = Field(
        default=["Room Rent", "PED Wait Time", "Co-Pay", "No Claim Bonus", "Daycare Limits"],
        description="The standard comparison metrics."
    )
    policy_a_scores: List[int] = Field(..., description="Scores for Policy A out of 100.")
    policy_b_scores: List[int] = Field(..., description="Scores for Policy B out of 100.")

class CompareResponse(BaseModel):
    policy_a_name: str
    policy_b_name: str
    winner: str
    chart_data: ChartMetrics
    executive_summary: str
    detailed_analysis: Dict[str, str]