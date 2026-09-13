from .base import BaseTool, ToolRegistry
from .code_analyzer import CodeAnalyzerTool
from .file_ops import FileReadTool, FileWriteTool
from .code_refactorer import CodeRefactorTool
from .lint_checker import LintCheckerTool
from .search_tool import SearchTool
from .test_runner import TestRunnerTool

def register_default_tools():
    """Registers standard tools in ToolRegistry."""
    ToolRegistry.register(CodeAnalyzerTool(), aliases=["analyze", "analyzer"])
    ToolRegistry.register(FileReadTool(), aliases=["read_file", "read", "cat"])
    ToolRegistry.register(FileWriteTool(), aliases=["write_file", "write"])
    ToolRegistry.register(CodeRefactorTool(), aliases=["refactor", "refactor_code"])
    ToolRegistry.register(LintCheckerTool(), aliases=["lint", "linter"])
    ToolRegistry.register(SearchTool(), aliases=["search", "find"])
    ToolRegistry.register(TestRunnerTool(), aliases=["test", "run_tests", "pytest"])

# Automatically register defaults upon package import
register_default_tools()

__all__ = [
    "BaseTool",
    "ToolRegistry",
    "CodeAnalyzerTool",
    "FileReadTool",
    "FileWriteTool",
    "CodeRefactorTool",
    "LintCheckerTool",
    "SearchTool",
    "TestRunnerTool",
    "register_default_tools",
]
