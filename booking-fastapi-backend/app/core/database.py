"""Database configuration and session management for the booking application.

This module sets up SQLAlchemy engine and session factory for database
connections, and provides a dependency injection function for FastAPI.

Configuration:
    DB_URL: MySQL connection string with credentials and database name.
    engine: SQLAlchemy engine instance for database operations.
    SessionLocal: Session factory for creating database sessions.
    Base: Declarative base class for ORM model definitions.
"""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

# Placeholder - replace with actual database credentials
DB_URL = "mysql+pymysql://api_user:api_password@localhost:3306/task_db"

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

# SQLAlchemy declarative base for model definitions
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Dependency injection function for database session.

    Provides a SQLAlchemy session for each request and ensures proper
    cleanup after the request is completed. This is used as a FastAPI
    dependency for accessing the database in endpoint handlers.

    Yields:
        Session: Database session for use in request handlers.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        # Close database connection
        db.close()
