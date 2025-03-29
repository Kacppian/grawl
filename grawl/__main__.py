import os
import sys
import typer
from rich.console import Console
from rich.progress import Progress
from typing import Optional

from grawl.utils.git import clone_repository
from grawl.agents.doc_generator import generate_documentation

app = typer.Typer(help="Grawl: Generate repository documentation for LLMs")
console = Console()

@app.callback()
def callback():
    """Grawl: Generate repository documentation for LLMs"""
    # Check if OPENAI_API_KEY is set
    if not os.environ.get("OPENAI_API_KEY"):
        console.print("[bold red]Error:[/bold red] OPENAI_API_KEY environment variable is not set.")
        console.print("Please set it using: export OPENAI_API_KEY='your-api-key'")
        sys.exit(1)

@app.command()
def generate(repo_url: str = typer.Argument(..., help="GitHub repository URL"),
            output_path: Optional[str] = typer.Option(None, "--output", "-o", help="Custom output path for documentation")):
    """Generate documentation for a GitHub repository"""
    console.print(f"[bold green]Grawl:[/bold green] Processing repository {repo_url}")
    
    # Extract repo name from URL
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    
    # Set paths
    repo_path = os.path.join(".grawl", "repositories", repo_name)
    
    if output_path is None:
        output_path = os.path.join(".grawl", "generated", f"{repo_name}.txt")
    
    # Clone repository
    with Progress() as progress:
        task = progress.add_task("[green]Cloning repository...", total=1)
        clone_repository(repo_url, repo_path)
        progress.update(task, advance=1)
    
    console.print(f"[bold green]Repository cloned to:[/bold green] {repo_path}")
    
    # Generate documentation
    with Progress() as progress:
        task = progress.add_task("[green]Generating documentation...", total=1)
        generate_documentation(repo_path, output_path)
        progress.update(task, advance=1)
    
    console.print(f"[bold green]Documentation generated at:[/bold green] {output_path}")

if __name__ == "__main__":
    app()
