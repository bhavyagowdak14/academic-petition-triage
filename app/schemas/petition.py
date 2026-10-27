from pydantic import BaseModel, Field
from typing import Optional


class PetitionRequest(BaseModel):
    student_id: str = Field(
        ..., min_length=1, description="Student identifier"
    )
    petition_type: str = Field(
        ..., min_length=1, description="Type of academic petition"
    )
    semester: int = Field(..., ge=1, le=12)
    reason: str = Field(
        ..., min_length=10, description="Reason for the petition"
    )
    attendance_percentage: Optional[float] = Field(
        default=None, ge=0, le=100
    )
    supporting_evidence: Optional[str] = None

