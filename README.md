# Repo-Rector

Repo-Rector is an AI-powered Python code improvement tool that uses Google's Gemini AI to clean up and enhance Python codebases. It analyzes your project's dependency graph and improves code for better readability and maintainability.

## Features

- **Code Cleanup**: Improves code clarity and structure
- **Bug Fixes**: Fixes obvious issues and inefficiencies
- **Readability**: Makes code more readable and maintainable
- **Dependency-Aware**: Uses the project's dependency graph to provide context for accurate improvements

## Prerequisites

- Python 3.8+
- A Google AI API key (Gemini)

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root and add your Google AI API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

## Usage

1. Place your Python project files in the same directory as `agent.py`
2. Run the improvement tool:
   ```bash
   python agent.py
   ```
3. The tool will analyze your code, build a dependency graph, and improve files starting from leaf nodes (files with no dependencies)

## Important Notes

- **Backup First**: This tool modifies your files in place. Make sure to backup your code before running.
- **Experimental**: The AI-generated improvements may not always be perfect. Review the changes before committing.
- **API Costs**: Using Google's Gemini API may incur costs based on your usage.

## Example

Before improvement:
```python
def calc(x,y):
    return x+y
```

After improvement:
```python
def calculate_sum(first_number, second_number):
    return first_number + second_number
```

## License

This project is open source. Please check the license file for details.