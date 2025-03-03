import os
import sys
import asyncio
import pathlib
from alembic import context
from dotenv import load_dotenv
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine

from app.db.database import Base  # Import the Base from your database module
from app.models import *  # Import your models for migrations


sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

# Load environment variables from .env file
load_dotenv()

# Fetch the database URL from the environment variable
db_url = os.getenv("DATABASE_URL")

if not db_url:
    raise ValueError("DATABASE_URL environment variable is not set!")

# Alembic Config object provides access to the values in the .ini file
config = context.config

# Interpret the config file for Python logging
fileConfig(config.config_file_name)

# The metadata for your models (SQLAlchemy)
target_metadata = Base.metadata

async def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = create_async_engine(db_url, echo=True, future=True)

    async with connectable.connect() as connection:
        # Run migrations with the connection in async context
        await connection.run_sync(do_run_migrations)

def do_run_migrations(connection):
    """Configure and run migrations for the given connection."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=db_url, target_metadata=target_metadata, literal_binds=True, compare_type=True, dialect_opts={"paramstyle": "named"}
    )

    with context.begin_transaction():
        context.run_migrations()

# If Alembic is running in offline mode (for generating migration files)
if context.is_offline_mode():
    run_migrations_offline()
else:
    # This runs the async migrations in the event loop
    asyncio.run(run_migrations_online())
