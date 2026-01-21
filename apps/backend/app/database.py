from sqlmodel import create_engine, Session, SQLModel
from typing import Generator
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/todo_db")

# Get environment setting (default to development)
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    echo=(ENVIRONMENT == "development"),  # Only log SQL in development
    pool_pre_ping=True,  # Verify connections before using
    pool_size=10,  # Number of connections to maintain
    max_overflow=20,  # Additional connections when pool is full
    pool_recycle=3600  # Recycle connections after 1 hour
)

def create_db_and_tables():
    """Create all database tables (use only for development/testing)"""
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """Dependency for FastAPI to get database session"""
    with Session(engine) as session:
        yield session
