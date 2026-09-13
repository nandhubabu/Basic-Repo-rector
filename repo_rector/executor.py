from typing import Any, Dict
from .models.task import PlanStep
from .models.tool_schema import ToolOutput
from .tools.base import ToolRegistry

class Executor:
    """Executes tools based on plan steps."""
    
    def __init__(self):
        # Tools are registered elsewhere and fetched from the registry
        pass
        
    def execute_step(self, step: PlanStep) -> ToolOutput:
        try:
            tool = ToolRegistry.get_tool(step.tool_name)
            
            # Validate input parameters against the tool's schema
            validated_params = tool.input_schema(**step.params)
            
            # Execute the tool
            result = tool.execute(**validated_params.model_dump())
            return result
        except ValueError as e:
            return ToolOutput(success=False, error=f"Validation error: {e}")
        except Exception as e:
            return ToolOutput(success=False, error=f"Execution error: {e}")
