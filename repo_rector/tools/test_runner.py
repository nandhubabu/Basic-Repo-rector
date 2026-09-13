import subprocess
from pydantic import BaseModel, Field
from .base import BaseTool
from ..models.tool_schema import ToolOutput

class TestRunnerInput(BaseModel):
    test_path: str = Field(default="tests/", description="Path to the tests directory or file")
    framework: str = Field(default="pytest", description="Testing framework to use (pytest, unittest)")

class TestRunnerTool(BaseTool):
    name = "test_runner"
    description = "Executes the test suite and returns the results."
    input_schema = TestRunnerInput
    
    def execute(self, test_path: str = "tests/", framework: str = "pytest") -> ToolOutput:
        try:
            if framework == "pytest":
                cmd = ["pytest", test_path, "-v"]
            elif framework == "unittest":
                cmd = ["python", "-m", "unittest", "discover", "-s", test_path]
            else:
                return ToolOutput(success=False, error=f"Unsupported testing framework: {framework}")
                
            process = subprocess.run(cmd, capture_output=True, text=True)
            
            # Subprocess exits with 0 on full success, 1 on test failures
            success = process.returncode == 0
            
            return ToolOutput(
                success=success, 
                data={
                    "stdout": process.stdout,
                    "stderr": process.stderr,
                    "returncode": process.returncode
                }
            )
        except Exception as e:
            return ToolOutput(success=False, error=str(e))
