import json
from typing import Dict, Any, List
from .models.task import Plan, PlanStep
from .llm.base import BaseLLMProvider
from .llm.prompt_templates import INTENT_ANALYSIS_PROMPT

class Planner:
    """Analyzes user intent and decomposes it into a structured plan."""
    
    def __init__(self, llm_provider: BaseLLMProvider):
        self.llm = llm_provider
        
    def create_plan(self, user_request: str, available_tools: Any, context: str = "") -> Plan:
        prompt = f"""
        User Request: {user_request}
        
        Available Tools:
        {json.dumps(available_tools, indent=2)}
        
        Context:
        {context}
        """
        
        response_text = self.llm.generate(
            prompt=prompt,
            system_prompt=INTENT_ANALYSIS_PROMPT,
            json_mode=True
        )
        
        try:
            plan_data = json.loads(response_text)
            
            steps = []
            for step_data in plan_data.get("steps", []):
                steps.append(PlanStep(
                    id=step_data["id"],
                    action=step_data["action"],
                    tool_name=step_data["tool_name"],
                    params=step_data.get("params", {}),
                    depends_on=step_data.get("depends_on", [])
                ))
                
            return Plan(
                intent=plan_data.get("intent", "unknown"),
                confidence=float(plan_data.get("confidence", 0.0)),
                steps=steps
            )
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse plan from LLM response: {e}")
