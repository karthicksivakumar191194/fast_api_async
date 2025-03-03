from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.settings import settings


# The URL to the database
SQLALCHEMY_DATABASE_URL = settings.database_url

# Create the SQLAlchemy async engine that connects to the database
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Create the session factory for creating async sessions
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
)

# Base class for your database models
Base = declarative_base()


# Dependency to get the current database session (async)
async def get_db():
    """
    Provides a database session, yielding it for use within a request context.
    After the request, the session is closed to free up resources.
    """
    async with SessionLocal() as session:  # Use async session context manager
        yield session  # Yield the async session to be used in a route or service
