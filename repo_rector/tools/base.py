from abc import ABC, abstractmethod
from typing import Type, Dict, Any
from pydantic import BaseModel
from ..models.tool_schema import ToolInput, ToolOutput

class BaseTool(ABC):
    """Abstract base class for all agent tools."""
    
    name: str
    description: str
    input_schema: Type[BaseModel]
    
    @abstractmethod
    def execute(self, **kwargs) -> ToolOutput:
        """Execute the tool with the provided arguments."""
        pass

class ToolRegistry:
    """Registry to hold and manage all available tools."""
    
    _tools: Dict[str, BaseTool] = {}
    
    @classmethod
    def register(cls, tool: BaseTool):
        cls._tools[tool.name] = tool
        
    @classmethod
    def get_tool(cls, name: str) -> BaseTool:
        if name not in cls._tools:
            raise ValueError(f"Tool '{name}' not found in registry.")
        return cls._tools[name]
        
    @classmethod
    def list_tools(cls) -> Dict[str, str]:
        return {name: tool.description for name, tool in cls._tools.items()}
