import json
from typing import Dict, Optional, Any
from ..models.agent_state import AgentState, AgentStatus
from ..models.task import Plan

class SessionManager:
    """Manages the current session state for the agent."""
    
    def __init__(self, session_id: str):
        self.state = AgentState(session_id=session_id)
        
    def set_plan(self, plan: Plan):
        self.state.current_plan = plan
        self.state.pending_steps = plan.steps.copy()
        
    def update_status(self, status: AgentStatus):
        self.state.status = status
        
    def add_error(self, error: str):
        self.state.errors.append(error)
        
    def to_json(self) -> str:
        return self.state.model_dump_json(indent=2)
        
    @classmethod
    def from_json(cls, json_str: str) -> "SessionManager":
        data = json.loads(json_str)
        instance = cls(session_id=data["session_id"])
        instance.state = AgentState(**data)
        return instance
