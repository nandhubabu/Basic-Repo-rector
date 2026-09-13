import os
import logging
from google import genai
from typing import Optional
from .base import BaseLLMProvider

# Silence Google GenAI automatic function calling warning on generate_content
logging.getLogger("google_genai.models").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

# High-quota free-tier models ordered by priority (Flash Lite offers 500 requests/day each)
FREE_TIER_MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.5-flash",
]

class GeminiProvider(BaseLLMProvider):
    """Google Gemini provider implementation with automated quota fallback."""
    
    def __init__(self, model_name: str = "gemini-3.5-flash-lite"):
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

        # Build candidate models starting with the chosen model followed by fallbacks
        candidates = [self.model_name] + [m for m in FREE_TIER_MODELS if m != self.model_name]
        last_error = None

        for model in candidates:
            try:
                response = self.client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=config_kwargs
                )
                # Keep the working model for future calls in this session
                self.model_name = model
                return response.text
            except Exception as e:
                err_str = str(e)
                if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str or "quota" in err_str.lower():
                    logger.warning(f"Model {model} hit quota/rate limit. Falling back to next available model...")
                    last_error = e
                    continue
                # For non-quota errors, raise immediately
                raise e

        raise last_error or RuntimeError("All free Gemini models exhausted their quota.")
