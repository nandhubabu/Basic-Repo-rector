import os
import shutil
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from .base import BaseTool
from ..models.tool_schema import ToolOutput

class FileReadInput(BaseModel):
    filepath: str = Field(default="", description="The path to the file to read")
    file_path: Optional[str] = None
    path: Optional[str] = None

class FileReadTool(BaseTool):
    name = "file_reader"
    description = "Reads the content of a file."
    input_schema = FileReadInput
    
    def execute(self, filepath: str = "", file_path: Optional[str] = None, path: Optional[str] = None) -> ToolOutput:
        target = filepath or file_path or path or ""
        try:
            if not target or not os.path.exists(target):
                return ToolOutput(success=False, error=f"File not found: {target}")
                
            with open(target, 'r', encoding='utf-8') as f:
                content = f.read()
            return ToolOutput(success=True, data={"content": content, "filepath": target})
        except Exception as e:
            return ToolOutput(success=False, error=str(e))

class FileWriteInput(BaseModel):
    filepath: str = Field(default="", description="The path to the file to write")
    file_path: Optional[str] = None
    path: Optional[str] = None
    content: str = Field(description="The content to write to the file")
    create_backup: bool = Field(default=True, description="Whether to create a .bak backup")

class FileWriteTool(BaseTool):
    name = "file_writer"
    description = "Writes content to a file, optionally creating a backup."
    input_schema = FileWriteInput
    
    def execute(self, filepath: str = "", file_path: Optional[str] = None, path: Optional[str] = None, content: str = "", create_backup: bool = True) -> ToolOutput:
        target = filepath or file_path or path or ""
        try:
            if not target:
                return ToolOutput(success=False, error="No filepath specified.")
            if create_backup and os.path.exists(target):
                shutil.copy2(target, f"{target}.bak")
                
            os.makedirs(os.path.dirname(os.path.abspath(target)), exist_ok=True)
            with open(target, 'w', encoding='utf-8') as f:
                f.write(content)
                
            return ToolOutput(success=True, data={"filepath": target, "bytes_written": len(content)})
        except Exception as e:
            return ToolOutput(success=False, error=str(e))
