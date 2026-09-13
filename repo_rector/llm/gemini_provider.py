import os
import logging
from google import genai
from typing import Optional
from .base import BaseLLMProvider

# Silence Google GenAI automatic function calling warning on generate_content
logging.getLogger("google_genai.models").setLevel(logging.ERROR)

class GeminiProvider(BaseLLMProvider):
    """Google Gemini provider implementation (Free tier capable)."""
    
    def __init__(self, model_name: str = "gemini-3.6-flash"):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is missing.")
        
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name

    def generate(self, prompt: str, system_prompt: Optional[str] = None, json_mode: bool = False, temperature: float = 0.7) -> str:
        config_kwargs = {"temperature": temperature}
        if system_prompt:
            config_kwargs["system_instruction"] = system_prompt
            
        if json_mode:
            config_kwargs["response_mime_type"] = "application/json"
            
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=config_kwargs
        )
        
        return response.text
