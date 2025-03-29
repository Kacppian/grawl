import os
import fnmatch
from pathlib import Path
from typing import List, Dict, Set, Tuple

# File Utilities
# ==============

def get_file_extension(file_path: str) -> str:
    """
    Retrieves the file extension from a given file path.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The file extension in lowercase.
    """
    return os.path.splitext(file_path)[1].lower()


def is_binary_file(file_path: str) -> bool:
    """
    Checks if a file is likely binary based on its extension.

    Args:
        file_path (str): The path to the file.

    Returns:
        bool: True if the file is likely binary, False otherwise.
    """
    binary_extensions = {
        '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.webp',  # Images
        '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',  # Documents
        '.zip', '.tar', '.gz', '.rar', '.7z',  # Archives
        '.exe', '.dll', '.so', '.dylib',  # Executables/libraries
        '.pyc', '.pyo', '.pyd',  # Python compiled
        '.o', '.a', '.lib',  # Object files
        '.mp3', '.mp4', '.avi', '.mov', '.flv', '.wav',  # Media
    }
    
    return get_file_extension(file_path) in binary_extensions


# Repository File Filtering
# ========================

def filter_repository_files(repo_path: str, max_size_kb: int = 1000) -> Tuple[List[str], List[str]]:
    """
    Filters repository files to include only relevant text files under a certain size.

    Args:
        repo_path (str): The path to the repository.
        max_size_kb (int, optional): The maximum file size in KB. Defaults to 1000.

    Returns:
        Tuple[List[str], List[str]]: A tuple containing the included files and excluded files.
    """
    included_files = []
    excluded_files = []
    
    # Common patterns to exclude
    exclude_patterns = [
        '*/node_modules/*', '*/venv/*', '*/.git/*', '*/.idea/*', '*/.vscode/*',
        '*/__pycache__/*', '*/build/*', '*/dist/*', '*/target/*',
        '*/.DS_Store', '*/Thumbs.db',
    ]
    
    for root, dirs, files in os.walk(repo_path):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, repo_path)
            
            # Check if file matches any exclude pattern
            if any(fnmatch.fnmatch(rel_path, pattern) for pattern in exclude_patterns):
                excluded_files.append(rel_path)
                continue
            
            # Skip hidden files
            if file.startswith('.'):
                excluded_files.append(rel_path)
                continue
            
            # Skip binary files
            if is_binary_file(file_path):
                excluded_files.append(rel_path)
                continue
            
            # Check file size
            try:
                size_kb = os.path.getsize(file_path) / 1024
                if size_kb > max_size_kb:
                    excluded_files.append(f"{rel_path} (too large: {size_kb:.2f} KB)")
                    continue
            except Exception:
                excluded_files.append(f"{rel_path} (error reading size)")
                continue
            
            included_files.append(rel_path)
    
    return included_files, excluded_files


# Important File Identification
# ===========================

def get_important_files(repo_path: str) -> Dict[str, List[str]]:
    """
    Identifies important files in the repository by category.

    Args:
        repo_path (str): The path to the repository.

    Returns:
        Dict[str, List[str]]: A dictionary mapping categories to lists of file paths.
    """
    important_files = {
        'documentation': [],
        'configuration': [],
        'package_management': [],
        'entry_points': [],
        'tests': [],
    }
    
    # Define patterns for each category
    patterns = {
        'documentation': ['README*', 'CONTRIBUTING*', 'CHANGELOG*', 'LICENSE*', 'docs/*', '*.md', '*.rst'],
        'configuration': ['.gitignore', '.env.example', '*.config.*', '*.conf', 'config/*', 'settings.*'],
        'package_management': ['setup.py', 'pyproject.toml', 'package.json', 'Cargo.toml', 'Gemfile', 'requirements.txt'],
        'entry_points': ['main.py', 'app.py', 'index.*', 'src/index.*', 'src/main.*'],
        'tests': ['test_*.py', '*_test.py', 'tests/*', 'spec/*'],
    }
    
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, repo_path)
            
            for category, category_patterns in patterns.items():
                if any(fnmatch.fnmatch(rel_path, pattern) for pattern in category_patterns):
                    important_files[category].append(rel_path)
    
    return important_files
