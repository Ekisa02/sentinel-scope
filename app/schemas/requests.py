from pydantic import BaseModel, HttpUrl
from typing import Optional


class ScanRequest(BaseModel):
    target: str
    simulate: Optional[bool] = True
    notes: Optional[str] = None
