import subprocess
from pydantic import BaseModel, Field
from .base import BaseTool
from ..models.tool_schema import ToolOutput

class LintCheckerInput(BaseModel):
    target_path: str = Field(default=".", description="Path to the directory or file to lint")
    linter: str = Field(default="flake8", description="Linter to use (flake8, pylint, ruff)")

class LintCheckerTool(BaseTool):
    name = "lint_checker"
    description = "Runs a linter on the specified path and returns the results."
    input_schema = LintCheckerInput
    
    def execute(self, target_path: str = ".", linter: str = "flake8") -> ToolOutput:
        try:
            if linter == "flake8":
                cmd = ["flake8", target_path]
            elif linter == "pylint":
                cmd = ["pylint", target_path]
            elif linter == "ruff":
                cmd = ["ruff", "check", target_path]
            else:
                return ToolOutput(success=False, error=f"Unsupported linter: {linter}")
                
            process = subprocess.run(cmd, capture_output=True, text=True)
            
            # Linters generally exit with 0 if no issues are found
            success = process.returncode == 0
            
            return ToolOutput(
                success=True, # We successfully ran the linter, even if it found issues
                data={
                    "issues_found": not success,
                    "stdout": process.stdout,
                    "stderr": process.stderr,
                    "returncode": process.returncode
                }
            )
        except Exception as e:
            return ToolOutput(success=False, error=str(e))
