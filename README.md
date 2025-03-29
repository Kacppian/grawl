# Grawl

A CLI tool that clones GitHub repositories and generates documentation for LLMs using OpenAI's agents framework.

## Installation

```bash
# Create a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Before using Grawl, you need to set your OpenAI API key:

```bash
export OPENAI_API_KEY='your-api-key'
```

## Usage

```bash
# Get help
python grawl.py --help

# Generate documentation for a GitHub repository
python grawl.py generate https://github.com/username/repository

# Specify a custom output path for documentation
python grawl.py generate https://github.com/username/repository --output custom_path.txt
```

## How it works

Grawl uses OpenAI's agents framework to:

1. Clone the specified GitHub repository to `.grawl/repositories/<repo_name>`
2. Analyze the repository structure and content
3. Generate comprehensive documentation in `.grawl/generated/<repo_name>.txt`

The documentation includes:
- Repository overview
- Architecture and components
- Key functionality
- API documentation
- Dependencies
- Usage examples
- Development guidelines

## Requirements

- Python 3.10+
- OpenAI API key
