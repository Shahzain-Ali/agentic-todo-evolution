"""
MCP Server Package

[Task]: T011
[From]: specs/003-ai-chatbot/spec.md §2, specs/003-ai-chatbot/plan.md §Phase 2

This package provides the MCP (Model Context Protocol) server for todo management.
It exposes 5 tools that the OpenAI Agent can call to interact with the todo database.
"""

from .server import mcp, get_db_session
from .config import config

__all__ = [
    "mcp",
    "get_db_session",
    "config",
]

__version__ = "0.1.0"
