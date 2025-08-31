import os
from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Student Performance Tracker API"
    debug: bool = True
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./students.db")

    @field_validator("database_url")
    @classmethod
    def normalize_sqlite(cls, v: str) -> str:
        # Ensure correct SQLite URL for SQLAlchemy when using relative path
        if v.startswith("sqlite") and ":///" in v and not v.startswith("sqlite+pysqlite"):
            # Modern SQLAlchemy prefers sqlite+pysqlite driver name
            v = v.replace("sqlite://", "sqlite+pysqlite://")
        return v


settings = Settings()
