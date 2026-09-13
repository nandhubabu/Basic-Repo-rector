import requests
from typing import Optional
from .base import BaseLLMProvider

class OllamaProvider(BaseLLMProvider):
    """Local Ollama provider implementation (Free)."""
    
    def __init__(self, model_name: str = "llama3", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url

    def generate(self, prompt: str, system_prompt: Optional[str] = None, json_mode: bool = False, temperature: float = 0.7) -> str:
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "temperature": temperature,
            "stream": False
        }
        
        if system_prompt:
            payload["system"] = system_prompt
            
        if json_mode:
            payload["format"] = "json"
            
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        return response.json().get("response", "")
