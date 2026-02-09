from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from dotenv import load_dotenv

from app.routers import auth, tasks, chatkit, demo

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Todo API",
    description="A modern full-stack todo application API with JWT authentication",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS Configuration
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

if ENVIRONMENT == "production":
    origins = [FRONTEND_URL]
else:
    origins = [
        FRONTEND_URL,
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3003",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(chatkit.router, prefix="/api", tags=["chatkit"])  # ChatKit endpoint at /api/chatkit
app.include_router(demo.router, prefix="/api/demo", tags=["demo"])  # Demo endpoints (no auth) for testing

@app.get("/health")
def health_check():
    """
    Health check endpoint for monitoring and load balancers.

    Returns:
        dict: Status information including API version
    """
    logger.info("Health check requested")
    return {
        "status": "healthy",
        "version": "1.0.0",
        "service": "todo-api"
    }

@app.get("/")
def root():
    """
    Root endpoint with API information.

    Returns:
        dict: Welcome message and documentation links
    """
    return {
        "message": "Todo API - A modern task management system",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }
