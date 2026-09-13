from abc import ABC, abstractmethod
from typing import Type, Dict, Any, Optional, List
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
    _aliases: Dict[str, str] = {
        "read_file": "file_reader",
        "read": "file_reader",
        "write_file": "file_writer",
        "write": "file_writer",
        "refactor": "code_refactorer",
        "refactor_code": "code_refactorer",
        "analyze": "code_analyzer",
        "analyzer": "code_analyzer",
        "lint": "lint_checker",
        "search": "search_tool",
        "test": "test_runner",
        "run_tests": "test_runner",
    }
    
    @classmethod
    def register(cls, tool: BaseTool, aliases: Optional[List[str]] = None):
        cls._tools[tool.name] = tool
        if aliases:
            for alias in aliases:
                cls._aliases[alias] = tool.name
        
    @classmethod
    def get_tool(cls, name: str) -> BaseTool:
        if name in cls._tools:
            return cls._tools[name]
        if name in cls._aliases and cls._aliases[name] in cls._tools:
            return cls._tools[cls._aliases[name]]
        raise ValueError(f"Tool '{name}' not found in registry. Available tools: {list(cls._tools.keys())}")
        
    @classmethod
    def list_tools(cls) -> Dict[str, str]:
        return {name: tool.description for name, tool in cls._tools.items()}

    @classmethod
    def list_tools_detailed(cls) -> List[Dict[str, Any]]:
        result = []
        for name, tool in cls._tools.items():
            schema_props = {}
            if hasattr(tool, "input_schema") and hasattr(tool.input_schema, "model_json_schema"):
                schema_props = tool.input_schema.model_json_schema().get("properties", {})
            result.append({
                "name": name,
                "description": tool.description,
                "parameters": {k: v.get("type", "string") for k, v in schema_props.items()}
            })
        return result
