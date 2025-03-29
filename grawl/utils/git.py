import os
import shutil
from git import Repo
from rich.console import Console
from typing import Optional

console = Console()


def clone_repository(repo_url: str, repo_path: str) -> str:
    """
    Clone a GitHub repository to the specified path.
    
    This function clones a Git repository from the provided URL to the specified
    local path. If the repository already exists at the destination, it will be
    removed and re-cloned.
    
    Args:
        repo_url: URL of the GitHub repository
        repo_path: Path where the repository should be cloned
        
    Returns:
        Path to the cloned repository
        
    Raises:
        Exception: If there's an error during the cloning process
    """
    try:
        # Check if repository directory already exists
        if os.path.exists(repo_path):
            console.print(f"[yellow]Repository already exists at {repo_path}. Removing and re-cloning...[/yellow]")
            shutil.rmtree(repo_path)
        
        # Create parent directories if they don't exist
        os.makedirs(os.path.dirname(repo_path), exist_ok=True)
        
        # Clone the repository
        Repo.clone_from(repo_url, repo_path)
        
        return repo_path
    except Exception as e:
        console.print(f"[bold red]Error cloning repository:[/bold red] {str(e)}")
        raise
