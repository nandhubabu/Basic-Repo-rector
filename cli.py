import os
import sys
import argparse
from dotenv import load_dotenv
load_dotenv()
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from repo_rector.orchestrator import Orchestrator

console = Console()

def print_banner():
    console.print(Panel.fit("[bold blue]CodeNova AI[/bold blue]\n[cyan]Your intelligent Python codebase agent[/cyan]"))

def chat_mode():
    console.print("[green]Entering chat mode. Type 'exit' or 'quit' to stop.[/green]\n")
    orchestrator = Orchestrator()
    
    while True:
        try:
            user_input = console.input("[bold yellow]You:[/bold yellow] ")
            if user_input.lower() in ['exit', 'quit']:
                break
                
            if not user_input.strip():
                continue
                
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                progress.add_task(description="Thinking...", total=None)
                response = orchestrator.run(user_input)
                
            console.print(f"\n[bold green]CodeNova:[/bold green] {response}\n")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

def single_run_mode(instruction: str):
    console.print(f"[yellow]Executing:[/yellow] {instruction}")
    orchestrator = Orchestrator()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Processing...", total=None)
        response = orchestrator.run(instruction)
        
    console.print(f"\n[bold green]Result:[/bold green]\n{response}")

def main():
    parser = argparse.ArgumentParser(description="Repo-Rector AI Agent")
    parser.add_argument("--chat", action="store_true", help="Start in interactive chat mode")
    parser.add_argument("--run", type=str, help="Run a single instruction and exit")
    
    args = parser.parse_args()
    
    print_banner()
    
    if args.run:
        single_run_mode(args.run)
    elif args.chat or len(sys.argv) == 1:
        # Default to chat mode if no args provided
        chat_mode()

if __name__ == "__main__":
    main()
