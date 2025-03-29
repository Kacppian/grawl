from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="grawl",
    version="0.1.0",
    author="Grawl Team",
    author_email="example@example.com",
    description="Generate repository documentation for LLMs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/grawl",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
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
    entry_points={
        "console_scripts": [
            "grawl=grawl.__main__:app",
        ],
    },
)
