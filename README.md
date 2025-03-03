# FastAPI Async Application

## Installation

1. Clone the repository:
    ```bash
      git clone https://github.com/karthicksivakumar191194/fast_api_async.git
    ```
    ```bash 
      cd fast_api_async
    ```

2. Check the Python version: Make sure your Python version is 3.9 or above. 
    ```bash
      python3 --version
    ```

3. Create and activate a virtual environment:
    ```bash
      python3 -m venv venv
    ```
    ```bash
      source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

4. Install the required dependencies:
    ```bash
      pip install -r requirements.txt
    ```

## Running the Application

You can start the FastAPI server using:
  ```bash
    python3 run.py
  ```
## Database Migrations

1. Creating a new Migration:
    ```bash
      alembic revision --autogenerate -m "migration description"
    ```

2. Apply the Migration
    ```bash
      alembic upgrade head
    ```

3. Roll Back a Migration
    ```bash
      alembic downgrade -1
   ```
   
## Code Formatting

Format all files in `app` directory:
  ```bash
    black app/
  ```

## Core Packages

```bash
    pip install fastapi[all] asyncpg sqlalchemy databases
```
* **fastapi[all]**
     - **Uvicorn**: For serving the FastAPI app.
     - **Pydantic**: For request and response data validation.
     - **SQLAlchemy**: For ORM-based database interaction (with async support if you use asyncpg or databases).
     - **Databases**: Async support for querying databases like PostgreSQL or SQLite asynchronously.
     - **HTTPX**: To make HTTP requests asynchronously (helpful for testing or calling external APIs).
     - **pytest**: Testing your FastAPI app.
* **asyncpg**: A driver for async PostgreSQL support.
* **sqlalchemy**: For ORM (Object-Relational Mapping) support.
* **databases**: For async database connections.

Manage database migrations
```bash
  pip install alembic
```
Initialize Alembic
```bash
  alembic init alembic
```
Import Application Models in env.py
```bash
  from app.models import *
```

Password hashing library
```bash
  pip install passlib[bcrypt]
```

Handle internationalization and localization tasks
```bash
  pip install Babel
```
Handle file I/O operations asynchronously
```bash
  pip install aiofiles
```

Rate-limiting library for FastAPI
```bash
    pip install slowapi
```

Python code formatter
```bash
    pip install black
```

Install pre-commit
```bash
    pip install pre-commit
```
Set up the Git hooks and prepare them to run before every commit.
```bash
    pre-commit install
```