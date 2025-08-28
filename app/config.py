import os
from typing import Optional

class Settings:
    """Application configuration settings"""
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "students.db")
    DATABASE_TYPE: str = os.getenv("DATABASE_TYPE", "sqlite")  # sqlite or postgresql
    
    # API settings
    API_TITLE: str = "Student Performance Tracker"
    API_VERSION: str = "1.0.0"
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    
    # Security settings
    SECRET_KEY: Optional[str] = os.getenv("SECRET_KEY")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # CORS settings
    CORS_ORIGINS: list = ["*"]  # Configure for production
    
    # Pagination settings
    DEFAULT_PAGE_SIZE: int = 10
    MAX_PAGE_SIZE: int = 100

settings = Settings()