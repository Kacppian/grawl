from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="grawl",
    version="0.1.0",
    author="Kacppian",
    author_email="aspkaushik@gmail.com",
    description="Generate repository documentation for LLMs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kacppian/grawl",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Documentation",
    ],
    python_requires=">=3.10",
    install_requires=[
        "openai>=1.10.0",
        "openai-agents==0.0.7",
        "typer>=0.9.0",
        "gitpython>=3.1.40",
        "rich>=13.6.0",
        "pydantic>=2.5.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "grawl=grawl.__main__:app",
        ],
    },
    project_urls={
        "Bug Tracker": "https://github.com/kacppian/grawl/issues",
        "Documentation": "https://github.com/kacppian/grawl#readme",
        "Source Code": "https://github.com/kacppian/grawl",
    },
)
