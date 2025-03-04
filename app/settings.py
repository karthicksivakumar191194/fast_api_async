from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    app_name: str = "FastAPI Async Application"
    environment: str = "local"  # local, development, qa, production
    secret_key: str
    allowed_hosts: List[str] = []
    google_sheet_credentials: str
    onboarded_tenant_list_gsheet_url: str

    # PostgreSQL Database
    database_url: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Initialize the settings
settings = Settings()
