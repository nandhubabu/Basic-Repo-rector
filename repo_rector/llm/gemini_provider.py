import os
import google.generativeai as genai
from typing import Optional
from .base import BaseLLMProvider

class GeminiProvider(BaseLLMProvider):
    """Google Gemini provider implementation (Free tier capable)."""
    
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is missing.")
        
        genai.configure(api_key=api_key)
        self.model_name = model_name

    def generate(self, prompt: str, system_prompt: Optional[str] = None, json_mode: bool = False, temperature: float = 0.7) -> str:
        # For Gemini 1.5/2.5 models, system instructions can be passed
        kwargs = {}
        if system_prompt:
            kwargs["system_instruction"] = system_prompt
            
        model = genai.GenerativeModel(
            model_name=self.model_name,
            **kwargs
        )
        
        generation_config = genai.types.GenerationConfig(
            temperature=temperature
        )
        if json_mode:
            generation_config.response_mime_type = "application/json"
            
        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )
        
        return response.text
