from pydantic import BaseModel
from pydantic import Field
from typing import List, Dict, Any

class Insight(BaseModel):
    summary: str
    key_trends: List[str]
    risks: List[str]
    recommendations: List[str]
    charts: Dict[str, str]  # chart name -> base64 string
    interactive: Dict[str, Any] = Field(default_factory=dict)
