import os


class Settings:
    # Database URL: SQLite by default, can be overridden with environment variable
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./students.db")
    DEBUG: bool = os.getenv("DEBUG", "True") == "True"
    APP_NAME: str = os.getenv("APP_NAME", "Student Performance Tracker API")


settings = Settings()
