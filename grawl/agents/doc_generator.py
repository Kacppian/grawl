import os
import json
from typing import List, Dict, Any, Optional
from pathlib import Path
from pydantic import BaseModel

from agents import Agent, function_tool, Runner
from rich.console import Console
from grawl.utils.file_utils import filter_repository_files, get_important_files

console = Console()


class FileContent(BaseModel):
    """Model representing file content information.

    Attributes:
        path: Path to the file
        content: Content of the file
        size: Size of the file in bytes
    """
    path: str
    content: str
    size: int


class RepoStructure(BaseModel):
    """Model representing repository structure.

    Attributes:
        files: List of file paths in the repository
        directories: List of directory paths in the repository
    """
    files: List[str]
    directories: List[str]


class DocGenerator(Agent):
    """Agent that generates documentation for a GitHub repository.
    
    This agent analyzes repository structure and content to generate
    comprehensive documentation optimized for LLMs.
    """
    pass


@function_tool
def list_directory(path: str) -> Dict[str, List[str]]:
    """List all files and directories in the given path.
    
    Args:
        path: Path to the directory to list
        
    Returns:
        Dictionary containing lists of files and directories
        
    Raises:
        Exception: If there's an error listing the directory
    """
    try:
        p = Path(path)
        files = []
        directories = []
        
        for item in p.iterdir():
            if item.name.startswith("."):
                continue  # Skip hidden files/directories
                
            if item.is_file():
                files.append(str(item))
            elif item.is_dir():
                directories.append(str(item))
        
        return {"files": files, "directories": directories}
    except Exception as e:
        console.print(f"[bold red]Error listing directory:[/bold red] {str(e)}")
        raise


@function_tool
def read_file(path: str, max_size_kb: int) -> Dict[str, Any]:
    """Read the content of a file if its size is less than max_size_kb.
    
    Args:
        path: Path to the file to read
        max_size_kb: Maximum file size in KB to read
        
    Returns:
        Dictionary containing file path, content, and size
        
    Raises:
        Exception: If there's an error reading the file
    """
    try:
        p = Path(path)
        size = p.stat().st_size
        size_kb = size / 1024
        
        if size_kb > max_size_kb:
            return {
                "path": path,
                "content": f"File too large to read ({size_kb:.2f} KB > {max_size_kb} KB)",
                "size": size
            }
        
        # Skip binary files and common non-text files
        if p.suffix.lower() in [".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".tar", ".gz", ".exe", ".dll"]:
            return {
                "path": path,
                "content": f"Binary file skipped ({p.suffix})",
                "size": size
            }
        
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            return {"path": path, "content": content, "size": size}
        except UnicodeDecodeError:
            return {
                "path": path,
                "content": "Binary file (failed UTF-8 decode)",
                "size": size
            }
    except Exception as e:
        console.print(f"[bold red]Error reading file:[/bold red] {str(e)}")
        raise


@function_tool
def get_repo_summary(repo_path: str) -> Dict[str, Any]:
    """Get a summary of the repository structure and key files.
    
    Args:
        repo_path: Path to the repository
        
    Returns:
        Dictionary containing repository summary information
        
    Raises:
        Exception: If there's an error getting the repository summary
    """
    try:
        repo = Path(repo_path)
        
        # Check for common files
        readme = None
        for readme_file in ["README.md", "README.rst", "README.txt", "README"]:
            readme_path = repo / readme_file
            if readme_path.exists():
                readme = str(readme_path)
                break
        
        # Look for package files
        package_files = []
        for pkg_file in ["setup.py", "pyproject.toml", "package.json", "Cargo.toml", "Gemfile"]:
            pkg_path = repo / pkg_file
            if pkg_path.exists():
                package_files.append(str(pkg_path))
        
        # Count files by type
        file_types = {}
        for item in repo.glob("**/*"):
            if item.is_file() and not any(p.startswith(".") for p in item.parts):
                ext = item.suffix.lower()
                if ext in file_types:
                    file_types[ext] += 1
                else:
                    file_types[ext] = 1
        
        return {
            "name": repo.name,
            "readme": readme,
            "package_files": package_files,
            "file_types": file_types,
        }
    except Exception as e:
        console.print(f"[bold red]Error getting repo summary:[/bold red] {str(e)}")
        raise


@function_tool
def filter_repo_files(repo_path: str, max_size_kb: int) -> Dict[str, Any]:
    """Filter repository files to include only relevant text files under a certain size.
    
    Args:
        repo_path: Path to the repository
        max_size_kb: Maximum file size in KB to include
        
    Returns:
        Dictionary containing included and excluded files information
        
    Raises:
        Exception: If there's an error filtering repository files
    """
    try:
        included_files, excluded_files = filter_repository_files(repo_path, max_size_kb)
        return {
            "included_files": included_files,
            "excluded_files": excluded_files,
            "included_count": len(included_files),
            "excluded_count": len(excluded_files)
        }
    except Exception as e:
        console.print(f"[bold red]Error filtering repository files:[/bold red] {str(e)}")
        raise


@function_tool
def get_key_files(repo_path: str) -> Dict[str, List[str]]:
    """Identify important files in the repository by category.
    
    Args:
        repo_path: Path to the repository
        
    Returns:
        Dictionary mapping categories to lists of file paths
        
    Raises:
        Exception: If there's an error getting key files
    """
    try:
        return get_important_files(repo_path)
    except Exception as e:
        console.print(f"[bold red]Error getting key files:[/bold red] {str(e)}")
        raise


def generate_documentation(repo_path: str, output_path: str) -> str:
    """Generate documentation for a repository using an OpenAI agent.
    
    Args:
        repo_path: Path to the repository
        output_path: Path where the documentation will be saved
        
    Returns:
        Path to the generated documentation
        
    Raises:
        Exception: If there's an error generating documentation
    """
    try:
        # Create agent
        console.print("[bold blue]Creating agent with gpt-4o-mini model...[/bold blue]")
        agent = DocGenerator(
            name="Documentation Generator",
            instructions="You are an expert developer tasked with creating comprehensive documentation for a GitHub repository. Focus on analyzing the repository structure, understanding key files, and documenting the main functionality. Be concise and structured in your analysis. Avoid going into excessive detail about individual files unless they are critical to understanding the codebase.",
            tools=[list_directory, read_file, get_repo_summary, filter_repo_files, get_key_files],
            model="gpt-4o-mini",
        )
        
        # Create prompt for the agent
        console.print("[bold blue]Preparing prompt for the agent...[/bold blue]")
        prompt = f"""Generate documentation for the GitHub repository at: {repo_path}
        
        Focus on:
        1. Repository overview and purpose
        2. Main components and structure
        3. Key functionality
        4. Important APIs and interfaces
        5. Dependencies
        
        Steps:
        1. First use get_repo_summary to understand the repository basics
        2. Use get_key_files to identify important files by category
        3. Use list_directory and read_file to examine key files
        4. Create a structured documentation that would help an LLM understand this codebase
        
        Keep your analysis concise and focused on the most important aspects of the codebase.
        """
        
        # Run the agent
        console.print("[bold green]Starting documentation generation...[/bold green]")
        try:
            console.print("[bold blue]Calling Runner.run_sync with max_turns=30...[/bold blue]")
            result = Runner.run_sync(agent, prompt, max_turns=30)
            console.print("[bold blue]Runner.run_sync completed successfully![/bold blue]")
        except Exception as e:
            console.print(f"[bold red]Error running agent:[/bold red] {str(e)}")
            raise
        console.print("[bold green]Documentation generation completed![/bold green]")
        
        # Save the documentation to the output file
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            f.write(result.final_output)
        
        return output_path
    except Exception as e:
        console.print(f"[bold red]Error generating documentation:[/bold red] {str(e)}")
        raise
