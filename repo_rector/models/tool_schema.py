from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

class ToolInput(BaseModel):
    """Base class for all tool inputs"""
    pass

class ToolOutput(BaseModel):
    """Base class for all tool outputs"""
    success: bool = Field(description="Whether the tool execution was successful")
    data: Optional[Dict[str, Any]] = Field(default=None, description="The output data from the tool")
    error: Optional[str] = Field(default=None, description="Error message if success is false")
