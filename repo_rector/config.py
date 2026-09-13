import os
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class AppConfig(BaseModel):
    # LLM settings
    default_llm_provider: str = Field(default="gemini")
    gemini_model: str = Field(default="gemini-3.6-flash")
    ollama_model: str = Field(default="llama3")
    groq_model: str = Field(default="llama3-8b-8192")
    
    # Memory settings
    db_path: str = Field(default="repo_rector_memory.db")
    chroma_path: str = Field(default="./.repo_rector_chroma")
    
    # Orchestrator settings
    max_iterations: int = Field(default=15)
    
    @classmethod
    def load_from_env(cls) -> "AppConfig":
        return cls(
            default_llm_provider=os.getenv("RR_LLM_PROVIDER", "gemini"),
            gemini_model=os.getenv("RR_GEMINI_MODEL", "gemini-3.6-flash"),
            ollama_model=os.getenv("RR_OLLAMA_MODEL", "llama3"),
            groq_model=os.getenv("RR_GROQ_MODEL", "llama3-8b-8192"),
            db_path=os.getenv("RR_DB_PATH", "repo_rector_memory.db"),
            chroma_path=os.getenv("RR_CHROMA_PATH", "./.repo_rector_chroma"),
            max_iterations=int(os.getenv("RR_MAX_ITERATIONS", "15"))
        )

# Global configuration instance
config = AppConfig.load_from_env()
