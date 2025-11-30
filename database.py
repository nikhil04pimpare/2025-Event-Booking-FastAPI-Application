"""Database configuration and session management for the booking application.

This module sets up SQLAlchemy engine and session factory for database
connections, and provides a dependency injection function for FastAPI.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base

# Placeholder - replace with actual database credentials
DB_URL = "mysql+pymysql://api_user:api_password@localhost:3306/task_db"

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

# it is for sqlalchemy classess declaration
Base = declarative_base()


def get_db():
    """Dependency injection function for database session.
    
    Provides a SQLAlchemy session for each request and ensures proper
    cleanup after the request is completed.
    
    Yields:
        Session: Database session for use in request handlers
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        # Close database connection
        db.close()
