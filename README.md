# CodeNova AI Agent

CodeNova is an AI-powered Python code improvement agent that uses a multi-tool architecture with planning, execution, and evaluation phases to intelligently refactor and manage your codebase.

## Architecture

The system follows an iterative agent loop:
**User Request → Intent Analysis → Task Planning → Tool Selection → Tool Execution → Result Evaluation → Next Action or Final Response**

It features:
- **Layered Memory**: Session state, short-term conversational context, and long-term ChromaDB vector storage.
- **Pluggable Tools**: Code analysis, file operations, search, linting, testing, and AI refactoring.
- **Swappable LLMs**: Supports Google Gemini (default), Ollama (local), and Groq.
- **Interfaces**: Rich CLI for terminal interaction and FastAPI for REST integrations.

## Prerequisites

- Python 3.8+
- An API key for your chosen LLM provider (e.g., `GOOGLE_API_KEY` or `GROQ_API_KEY`)

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your environment variables (e.g., in a `.env` file or exported to your shell):
   ```bash
   export GOOGLE_API_KEY=your_gemini_api_key
   # or
   export GROQ_API_KEY=your_groq_api_key
   ```

## Usage

### CLI Chat Mode
Interact with the agent in a conversational interface:
```bash
python cli.py --chat
```

### Single Instruction Mode
Run a specific instruction and exit:
```bash
python cli.py --run "Refactor the config.py file to use environment variables"
```

### FastAPI Server
Run the agent as a REST API:
```bash
python server.py
```
Then navigate to `http://localhost:8000/docs` to interact with the API endpoints.

## License

This project is open source. Please check the license file for details.