import ast
import os
from typing import Dict, List, Any
from pydantic import BaseModel, Field
from .base import BaseTool
from ..models.tool_schema import ToolOutput

class CodeAnalyzerInput(BaseModel):
    directory: str = Field(default=".", description="The directory to analyze")

class DependencyFinder(ast.NodeVisitor):
    def __init__(self):
        self.found_imports = []

    def visit_Import(self, node):
        for alias in node.names:
            self.found_imports.append(alias.name)

    def visit_ImportFrom(self, node):
        if node.module:
            self.found_imports.append(node.module)

class CodeAnalyzerTool(BaseTool):
    name = "code_analyzer"
    description = "Analyzes a Python directory and builds a dependency graph."
    input_schema = CodeAnalyzerInput
    
    def execute(self, directory: str = ".") -> ToolOutput:
        try:
            project_graph = {}
            for root, _, files in os.walk(directory):
                for file in files:
                    if file.endswith(".py"):
                        filepath = os.path.join(root, file)
                        try:
                            with open(filepath, 'r', encoding='utf-8') as f:
                                tree = ast.parse(f.read())
                                
                            finder = DependencyFinder()
                            finder.visit(tree)
                            project_graph[filepath] = finder.found_imports
                        except Exception:
                            pass # Skip files that can't be parsed
                            
            return ToolOutput(success=True, data={"graph": project_graph})
        except Exception as e:
            return ToolOutput(success=False, error=str(e))
