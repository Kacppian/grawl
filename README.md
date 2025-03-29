# Grawl

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)

A CLI tool that clones GitHub repositories and generates comprehensive documentation for LLMs using OpenAI's agents framework.

## Features

- Clone GitHub repositories to a local directory
- Analyze repository structure and content
- Generate comprehensive documentation optimized for LLMs
- Identify important files and components
- Filter out binary and irrelevant files

## Installation

### From PyPI (Recommended)

```bash
pip install grawl
```

### From Source

```bash
# Clone the repository
git clone https://github.com/kacppian/grawl.git
cd grawl

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e .
```

## Configuration

Before using Grawl, you need to set your OpenAI API key:

```bash
export OPENAI_API_KEY='your-api-key'
```

On Windows:

```cmd
set OPENAI_API_KEY=your-api-key
```

## Usage

### Command Line Interface

```bash
# Get help
grawl --help

# Generate documentation for a GitHub repository
grawl generate https://github.com/username/repository

# Specify a custom output path for documentation
grawl generate https://github.com/username/repository --output custom_path.txt
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

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/kacppian/grawl.git
cd grawl

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Requirements

- Python 3.10+
- OpenAI API key
