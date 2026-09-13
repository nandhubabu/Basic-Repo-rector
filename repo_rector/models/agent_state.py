from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from .task import Plan, PlanStep
from .tool_schema import ToolOutput

class AgentStatus(str, Enum):
    IDLE = "IDLE"
    ANALYZING = "ANALYZING"
    PLANNING = "PLANNING"
    EXECUTING = "EXECUTING"
    EVALUATING = "EVALUATING"
    RESPONDING = "RESPONDING"
    ERROR = "ERROR"
    COMPLETED = "COMPLETED"

class AgentState(BaseModel):
    """Represents the complete state of an agent execution session"""
    session_id: str
    status: AgentStatus = AgentStatus.IDLE
    current_plan: Optional[Plan] = None
    completed_steps: List[PlanStep] = Field(default_factory=list)
    pending_steps: List[PlanStep] = Field(default_factory=list)
    tool_results: Dict[str, ToolOutput] = Field(default_factory=dict)
    errors: List[str] = Field(default_factory=list)
    iteration_count: int = 0
    max_iterations: int = 15
    context: Dict[str, Any] = Field(default_factory=dict, description="Arbitrary context data")
