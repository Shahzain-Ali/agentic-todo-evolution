"""
MCP Server Initialization

[Task]: T010
[From]: specs/003-ai-chatbot/spec.md §2, specs/003-ai-chatbot/plan.md §Phase 2

This module initializes the MCP server with FastMCP, sets up database connections,
and registers all MCP tools for todo management.
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastmcp import FastMCP
from sqlmodel import create_engine, Session
from sqlalchemy.pool import StaticPool

from .config import config

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Database engine (shared with FastAPI app)
engine = None


@asynccontextmanager
async def lifespan(server: FastMCP) -> AsyncGenerator[None, None]:
    """
    Lifespan context manager for MCP server

    Handles:
    - Database connection initialization
    - Configuration validation
    - Resource cleanup on shutdown
    """
    global engine

    logger.info("Starting MCP server...")

    # Validate configuration
    try:
        config.validate()
        logger.info("Configuration validated successfully")
    except ValueError as e:
        logger.error(f"Configuration validation failed: {e}")
        raise

    # Initialize database engine
    try:
        engine = create_engine(
            config.DATABASE_URL,
            echo=False,  # Set to True for SQL debugging
            connect_args={"check_same_thread": False} if "sqlite" in config.DATABASE_URL else {},
            poolclass=StaticPool if "sqlite" in config.DATABASE_URL else None
        )
        logger.info(f"Database engine initialized: {config.DATABASE_URL[:20]}...")
    except Exception as e:
        logger.error(f"Failed to initialize database engine: {e}")
        raise

    logger.info(f"MCP server '{config.SERVER_NAME}' v{config.SERVER_VERSION} ready")
    logger.info(f"Listening on {config.HOST}:{config.PORT}")

    yield  # Server is running

    # Cleanup on shutdown
    logger.info("Shutting down MCP server...")
    if engine:
        engine.dispose()
        logger.info("Database connections closed")

    logger.info("MCP server shutdown complete")


# Initialize FastMCP server
mcp = FastMCP(
    name=config.SERVER_NAME,
    version=config.SERVER_VERSION,
    lifespan=lifespan
)


def get_db_session() -> Session:
    """
    Get database session for MCP tools

    Returns:
        SQLModel Session instance
    """
    if not engine:
        raise RuntimeError("Database engine not initialized")

    return Session(engine)


# Tool registration
# Import tools as they are implemented
from .tools.add_task import add_task
from .tools.list_tasks import list_tasks
from .tools.complete_task import complete_task
# from .tools.delete_task import delete_task
# from .tools.update_task import update_task

# Register tools with MCP server
mcp.tool()(add_task)
mcp.tool()(list_tasks)
mcp.tool()(complete_task)
# mcp.tool()(delete_task)
# mcp.tool()(update_task)

# Create ASGI app using FastAPI wrapper for deployment compatibility
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="MCP Todo Server")

# CORS for external access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"service": "MCP Todo Server", "status": "running", "version": config.SERVER_VERSION}

@app.get("/health")
def health():
    return {"status": "healthy"}

# Mount FastMCP SSE app
try:
    mcp_app = mcp.http_app()
    app.mount("/mcp", mcp_app)
    logger.info("MCP app mounted at /mcp")
except Exception as e:
    logger.warning(f"Could not mount MCP app: {e}")


if __name__ == "__main__":
    # Run MCP server
    import uvicorn

    logger.info("Starting MCP server via uvicorn...")

    uvicorn.run(
        "mcp_server.server:app",
        host=config.HOST,
        port=config.PORT,
        reload=True if config.LOG_LEVEL == "DEBUG" else False
    )
