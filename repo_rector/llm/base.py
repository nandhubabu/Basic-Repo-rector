from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseLLMProvider(ABC):
    """Abstract base class for all LLM providers (Gemini, Groq, Ollama)."""
    
    @abstractmethod
    def generate(self, prompt: str, system_prompt: Optional[str] = None, json_mode: bool = False, temperature: float = 0.7) -> str:
        """
        Generate text from the LLM.
        
        Args:
            prompt: The user prompt to send
            system_prompt: Optional system instruction
            json_mode: Whether to enforce JSON output formatting
            temperature: Sampling temperature
            
        Returns:
            The generated string (potentially a JSON string)
        """
        pass
