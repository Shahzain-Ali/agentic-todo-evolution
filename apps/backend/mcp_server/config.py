"""
MCP Server Configuration

[Task]: T007
[From]: specs/003-ai-chatbot/spec.md §2 (Requirements), specs/003-ai-chatbot/plan.md §Phase 1
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class MCPConfig:
    """Configuration for MCP server"""

    # Server Settings
    HOST: str = os.getenv("MCP_SERVER_HOST", "localhost")
    PORT: int = int(os.getenv("MCP_SERVER_PORT", "8001"))

    # Database Settings (reuse from Phase 2)
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost:5432/todo_db"
    )

    # OpenAI Settings
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")

    # Security Settings
    JWT_SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    JWT_ALGORITHM: str = os.getenv("ALGORITHM", "HS256")

    # MCP Server Settings
    SERVER_NAME: str = "todo-mcp-server"
    SERVER_VERSION: str = "0.1.0"

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    @classmethod
    def validate(cls) -> None:
        """Validate required configuration"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        if not cls.JWT_SECRET_KEY:
            raise ValueError("SECRET_KEY environment variable is required")
        if not cls.DATABASE_URL:
            raise ValueError("DATABASE_URL environment variable is required")


# Create singleton instance
config = MCPConfig()
