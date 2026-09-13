from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field
from .task import PlanStep

class EvalDecision(str, Enum):
    SUFFICIENT = "SUFFICIENT"
    NEED_MORE_INFO = "NEED_MORE_INFO"
    CALL_ANOTHER_TOOL = "CALL_ANOTHER_TOOL"
    REVISE_PLAN = "REVISE_PLAN"
    ABORT = "ABORT"

class EvaluationResult(BaseModel):
    decision: EvalDecision = Field(description="The decision made by the evaluator")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence in the decision")
    reasoning: str = Field(description="Explanation of why this decision was made")
    suggested_next_step: Optional[PlanStep] = Field(default=None, description="Suggested next step if plan revision is needed")
    warnings: List[str] = Field(default_factory=list, description="Any warnings or issues detected")
