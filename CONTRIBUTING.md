# Contributing to Grawl

Thank you for considering contributing to Grawl! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## How Can I Contribute?

### Reporting Bugs

Bugs are tracked as GitHub issues. Create an issue and provide the following information:

- Use a clear and descriptive title
- Describe the exact steps to reproduce the bug
- Provide specific examples to demonstrate the steps
- Describe the behavior you observed after following the steps
- Explain which behavior you expected to see instead and why
- Include screenshots if possible

### Suggesting Enhancements

Enhancement suggestions are also tracked as GitHub issues. When creating an enhancement suggestion, please include:

- A clear and descriptive title
- A detailed description of the proposed enhancement
- An explanation of why this enhancement would be useful to most Grawl users

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests to ensure they pass
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

```bash
# Clone your fork of the repository
git clone https://github.com/YOUR_USERNAME/grawl.git
cd grawl

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

## Coding Style

We use [Black](https://black.readthedocs.io/) for code formatting and [isort](https://pycqa.github.io/isort/) for import sorting:

```bash
# Format code
black .

# Sort imports
isort .
```

We also use [flake8](https://flake8.pycqa.org/) for linting:

```bash
flake8 .
```

## Testing

We use [pytest](https://docs.pytest.org/) for testing:

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=grawl tests/
```

## Documentation

Please document all functions, classes, and modules using docstrings following the [Google style guide](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).

## Commit Messages

Please write clear and descriptive commit messages that explain the changes you've made.

## Thank You!

Thank you for contributing to Grawl!
