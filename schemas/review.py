from pydantic import BaseModel
from typing import Literal


class ReviewFinding(BaseModel):
    severity: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    category: Literal["security", "error_handling", "testing"]
    file: str
    line: int
    issue: str
    explanation: str
    suggested_fix: str
