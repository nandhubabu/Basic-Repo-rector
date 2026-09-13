from typing import Dict, Any, Optional
import uuid
from .models.agent_state import AgentStatus
from .models.evaluation import EvalDecision
from .memory.session_state import SessionManager
from .memory.short_term import ShortTermMemory
from .memory.long_term import LongTermMemory
from .planner import Planner
from .executor import Executor
from .evaluator import Evaluator
from .llm.gemini_provider import GeminiProvider
from .tools.base import ToolRegistry

class Orchestrator:
    """Main controller for the iterative agent loop."""
    
    def __init__(self, session_id: Optional[str] = None):
        self.session_id = session_id or str(uuid.uuid4())
        self.session = SessionManager(self.session_id)
        self.short_term = ShortTermMemory()
        self.long_term = LongTermMemory()
        
        # Initialize default provider (Gemini free tier)
        self.llm = GeminiProvider()
        
        self.planner = Planner(self.llm)
        self.executor = Executor()
        self.evaluator = Evaluator(self.llm)
        
    def run(self, user_request: str) -> str:
        self.short_term.add_interaction("user", user_request)
        self.session.update_status(AgentStatus.ANALYZING)
        
        try:
            # 1. Analyze Intent & Plan
            self.session.update_status(AgentStatus.PLANNING)
            available_tools = ToolRegistry.list_tools()
            plan = self.planner.create_plan(
                user_request=user_request, 
                available_tools=available_tools,
                context=self.short_term.get_context_string()
            )
            self.session.set_plan(plan)
            
            # 2. Execution Loop
            self.session.update_status(AgentStatus.EXECUTING)
            
            while self.session.state.pending_steps and self.session.state.iteration_count < self.session.state.max_iterations:
                self.session.state.iteration_count += 1
                
                # Get next step (simplified: just taking the first pending step)
                current_step = self.session.state.pending_steps.pop(0)
                current_step.status = "running"
                
                # Execute
                result = self.executor.execute_step(current_step)
                
                # Evaluate
                self.session.update_status(AgentStatus.EVALUATING)
                eval_result = self.evaluator.evaluate(
                    step=current_step, 
                    result=result,
                    context=self.short_term.get_context_string()
                )
                
                # Handle evaluation decision
                if eval_result.decision == EvalDecision.SUFFICIENT:
                    current_step.status = "completed"
                    self.session.state.completed_steps.append(current_step)
                    self.session.update_status(AgentStatus.EXECUTING) # Go back to executing next step
                    
                elif eval_result.decision == EvalDecision.REVISE_PLAN:
                    current_step.status = "failed"
                    current_step.error = eval_result.reasoning
                    self.session.add_error(f"Failed step {current_step.id}: {eval_result.reasoning}")
                    
                    # Need to implement plan revision logic here in a full system
                    # For now, we'll just abort the current loop
                    break
                    
                elif eval_result.decision == EvalDecision.ABORT:
                    self.session.add_error(f"Agent aborted: {eval_result.reasoning}")
                    break
                    
            self.session.update_status(AgentStatus.RESPONDING)
            final_response = f"Completed {len(self.session.state.completed_steps)} steps. Check logs for details."
            self.short_term.add_interaction("assistant", final_response)
            
            self.session.update_status(AgentStatus.COMPLETED)
            return final_response
            
        except Exception as e:
            self.session.update_status(AgentStatus.ERROR)
            self.session.add_error(str(e))
            return f"An error occurred: {e}"
