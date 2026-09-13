import os
import shutil
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from .base import BaseTool
from ..models.tool_schema import ToolOutput

class FileReadInput(BaseModel):
    filepath: str = Field(description="The path to the file to read")

class FileReadTool(BaseTool):
    name = "file_reader"
    description = "Reads the content of a file."
    input_schema = FileReadInput
    
    def execute(self, filepath: str) -> ToolOutput:
        try:
            if not os.path.exists(filepath):
                return ToolOutput(success=False, error=f"File not found: {filepath}")
                
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            return ToolOutput(success=True, data={"content": content})
        except Exception as e:
            return ToolOutput(success=False, error=str(e))

class FileWriteInput(BaseModel):
    filepath: str = Field(description="The path to the file to write")
    content: str = Field(description="The content to write to the file")
    create_backup: bool = Field(default=True, description="Whether to create a .bak backup")

class FileWriteTool(BaseTool):
    name = "file_writer"
    description = "Writes content to a file, optionally creating a backup."
    input_schema = FileWriteInput
    
    def execute(self, filepath: str, content: str, create_backup: bool = True) -> ToolOutput:
        try:
            if create_backup and os.path.exists(filepath):
                shutil.copy2(filepath, f"{filepath}.bak")
                
            os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
                
            return ToolOutput(success=True, data={"filepath": filepath, "bytes_written": len(content)})
        except Exception as e:
            return ToolOutput(success=False, error=str(e))
