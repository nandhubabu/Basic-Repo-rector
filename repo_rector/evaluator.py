import json
from .models.task import PlanStep
from .models.tool_schema import ToolOutput
from .models.evaluation import EvaluationResult, EvalDecision
from .llm.base import BaseLLMProvider
from .llm.prompt_templates import EVALUATION_PROMPT

class Evaluator:
    """Evaluates the result of a tool execution and decides the next step."""
    
    def __init__(self, llm_provider: BaseLLMProvider):
        self.llm = llm_provider
        
    def evaluate(self, step: PlanStep, result: ToolOutput, context: str = "") -> EvaluationResult:
        if not result.success:
            return EvaluationResult(
                decision=EvalDecision.REVISE_PLAN,
                confidence=1.0,
                reasoning=f"Tool execution failed: {result.error}",
                warnings=[result.error] if result.error else []
            )
            
        prompt = f"""
        Action Taken: {step.action}
        Tool Used: {step.tool_name}
        
        Tool Output:
        {json.dumps(result.data, indent=2)}
        
        Context:
        {context}
        """
        
        response_text = self.llm.generate(
            prompt=prompt,
            system_prompt=EVALUATION_PROMPT,
            json_mode=True
        )
        
        try:
            eval_data = json.loads(response_text)
            return EvaluationResult(
                decision=EvalDecision(eval_data.get("decision", "SUFFICIENT")),
                confidence=float(eval_data.get("confidence", 0.0)),
                reasoning=eval_data.get("reasoning", "No reasoning provided"),
                warnings=eval_data.get("warnings", [])
            )
        except json.JSONDecodeError as e:
            return EvaluationResult(
                decision=EvalDecision.REVISE_PLAN,
                confidence=0.0,
                reasoning=f"Failed to parse evaluation response: {e}"
            )
