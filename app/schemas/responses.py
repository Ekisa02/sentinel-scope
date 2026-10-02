from pydantic import BaseModel
from typing import List, Optional


class Finding(BaseModel):
    id: str
    type: str
    description: str
    confidence: float
    severity: Optional[str] = None


class ScanResult(BaseModel):
    job_id: str
    target: str
    findings: List[Finding]
