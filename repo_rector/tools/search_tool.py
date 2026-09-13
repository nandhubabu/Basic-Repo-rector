import os
import re
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from .base import BaseTool
from ..models.tool_schema import ToolOutput

class SearchInput(BaseModel):
    query: str = Field(description="The text or regex pattern to search for")
    directory: str = Field(default=".", description="Directory to search in")
    is_regex: bool = Field(default=False, description="Whether the query is a regular expression")
    file_extension: str = Field(default=".py", description="Filter by file extension")

class SearchTool(BaseTool):
    name = "search_tool"
    description = "Searches for text or patterns in the codebase."
    input_schema = SearchInput
    
    def execute(self, query: str, directory: str = ".", is_regex: bool = False, file_extension: str = ".py") -> ToolOutput:
        try:
            results = []
            
            pattern = re.compile(query) if is_regex else None
            
            for root, _, files in os.walk(directory):
                for file in files:
                    if not file.endswith(file_extension):
                        continue
                        
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            lines = f.readlines()
                            
                        for i, line in enumerate(lines):
                            match = False
                            if is_regex and pattern.search(line):
                                match = True
                            elif not is_regex and query in line:
                                match = True
                                
                            if match:
                                results.append({
                                    "file": filepath,
                                    "line_number": i + 1,
                                    "content": line.strip()
                                })
                    except Exception:
                        pass
                        
            return ToolOutput(success=True, data={"matches": results, "count": len(results)})
        except Exception as e:
            return ToolOutput(success=False, error=str(e))
