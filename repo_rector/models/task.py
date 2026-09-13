from datetime import datetime
from typing import List, Literal, Optional, Any, Dict
from pydantic import BaseModel, Field

class PlanStep(BaseModel):
    id: int
    action: str = Field(description="A descriptive name for the action to be taken")
    tool_name: str = Field(description="The name of the tool to execute this step")
    params: Dict[str, Any] = Field(default_factory=dict, description="Parameters to pass to the tool")
    depends_on: List[int] = Field(default_factory=list, description="IDs of steps that must complete before this one")
    status: Literal["pending", "running", "completed", "failed", "skipped"] = "pending"
    result: Optional[Any] = None
    error: Optional[str] = None

class Plan(BaseModel):
    intent: str = Field(description="The overall intent of the user request")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence in the plan")
    steps: List[PlanStep] = Field(default_factory=list, description="List of steps to execute")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    revision: int = 0
