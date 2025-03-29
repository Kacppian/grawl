"""Agents package for Grawl.

This package contains the agents used by Grawl to generate documentation
for GitHub repositories using OpenAI's agents framework.
"""

from grawl.agents.doc_generator import DocGenerator, generate_documentation

__all__ = ["DocGenerator", "generate_documentation"]
