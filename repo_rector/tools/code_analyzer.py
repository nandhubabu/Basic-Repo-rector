import ast
import os
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from .base import BaseTool
from ..models.tool_schema import ToolOutput

class CodeAnalyzerInput(BaseModel):
    path: str = Field(default=".", description="The directory or python file to analyze")
    directory: Optional[str] = None
    filepath: Optional[str] = None

    def target_path(self) -> str:
        return self.filepath or self.directory or self.path

class ASTInspector(ast.NodeVisitor):
    def __init__(self):
        self.imports = []
        self.classes = []
        self.functions = []

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append(alias.name)

    def visit_ImportFrom(self, node):
        if node.module:
            self.imports.append(node.module)

    def visit_ClassDef(self, node):
        methods = [m.name for m in node.body if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef))]
        self.classes.append({
            "name": node.name,
            "line": node.lineno,
            "methods": methods
        })
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.functions.append({
            "name": node.name,
            "line": node.lineno,
            "args": [arg.arg for arg in node.args.args]
        })
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self.functions.append({
            "name": node.name,
            "line": node.lineno,
            "args": [arg.arg for arg in node.args.args],
            "async": True
        })
        self.generic_visit(node)

class CodeAnalyzerTool(BaseTool):
    name = "code_analyzer"
    description = "Analyzes a Python file or directory, extracting AST structure (classes, functions, imports, dependencies)."
    input_schema = CodeAnalyzerInput
    
    def execute(self, path: str = ".", directory: Optional[str] = None, filepath: Optional[str] = None) -> ToolOutput:
        try:
            target = filepath or directory or path
            if not os.path.exists(target):
                return ToolOutput(success=False, error=f"Path not found: {target}")

            files_to_analyze = []
            if os.path.isfile(target):
                files_to_analyze.append(target)
            else:
                for root, _, files in os.walk(target):
                    for file in files:
                        if file.endswith(".py"):
                            files_to_analyze.append(os.path.join(root, file))

            analysis = {}
            for fp in files_to_analyze:
                try:
                    with open(fp, 'r', encoding='utf-8') as f:
                        code = f.read()
                    tree = ast.parse(code)
                    inspector = ASTInspector()
                    inspector.visit(tree)
                    analysis[fp] = {
                        "imports": inspector.imports,
                        "classes": inspector.classes,
                        "functions": inspector.functions,
                        "lines_of_code": len(code.splitlines())
                    }
                except Exception as e:
                    analysis[fp] = {"error": str(e)}

            return ToolOutput(success=True, data={"files_analyzed": len(analysis), "analysis": analysis})
        except Exception as e:
            return ToolOutput(success=False, error=str(e))

