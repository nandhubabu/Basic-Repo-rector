from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from .base import BaseTool
from ..models.tool_schema import ToolOutput
from ..llm.base import BaseLLMProvider

class CodeRefactorInput(BaseModel):
    filepath: str = Field(default="", description="The path to the file to refactor")
    file_path: Optional[str] = None
    path: Optional[str] = None
    context: Optional[str] = Field(default="", description="Additional context to provide to the LLM")
    provider_name: str = Field(default="gemini", description="LLM provider to use (gemini, ollama, groq)")

class CodeRefactorTool(BaseTool):
    name = "code_refactorer"
    description = "Refactors Python code using an LLM."
    input_schema = CodeRefactorInput
    
    def __init__(self, llm_providers: Optional[Dict[str, BaseLLMProvider]] = None):
        self.providers = llm_providers or {}
    
    def execute(self, filepath: str = "", file_path: Optional[str] = None, path: Optional[str] = None, context: str = "", provider_name: str = "gemini") -> ToolOutput:
        target = filepath or file_path or path or ""
        try:
            if not target or not os.path.exists(target):
                return ToolOutput(success=False, error=f"File not found: {target}")

            if provider_name not in self.providers:
                # Fallback to default Gemini provider
                from ..llm.gemini_provider import GeminiProvider
                self.providers["gemini"] = GeminiProvider()
                
            provider = self.providers.get(provider_name, self.providers.get("gemini"))
            if not provider:
                return ToolOutput(success=False, error=f"Provider '{provider_name}' not available.")
            
            with open(target, 'r', encoding='utf-8') as f:
                code = f.read()
                
            prompt = f"Context:\n{context}\n\nCode to refactor:\n{code}"
            system_prompt = "You are an expert Python code simplifier and refactorer. Rewrite the code to be cleaner, more maintainable, and adhere to PEP 8 standards. Return ONLY the raw python code."
            
            refactored_code = provider.generate(prompt=prompt, system_prompt=system_prompt)
            
            # Clean up potential markdown formatting
            if refactored_code.startswith("```python"):
                refactored_code = refactored_code.split("```python", 1)[1]
            if refactored_code.endswith("```"):
                refactored_code = refactored_code.rsplit("```", 1)[0]
            refactored_code = refactored_code.strip()
            
            return ToolOutput(success=True, data={"refactored_code": refactored_code, "filepath": target})
        except Exception as e:
            return ToolOutput(success=False, error=str(e))
