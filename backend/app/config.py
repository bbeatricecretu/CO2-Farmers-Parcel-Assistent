from pydantic_settings import BaseSettings
import os
from pathlib import Path
from typing import Optional

# Get the backend directory (parent of app folder)
BACKEND_DIR = Path(__file__).parent.parent
DB_PATH = BACKEND_DIR / "farmers.sqlite"

class Settings(BaseSettings):
    DATABASE_URL: str = f"sqlite:///{DB_PATH}"
    
    # LLM Configuration (Optional)
    USE_LLM: str = "false"
    LLM_PROVIDER: str = "gemini"
    LLM_API_KEY: Optional[str] = None
    LLM_MODEL: str = "gemini-1.5-flash"  # Default model, can be overridden in .env (e.g., gemma-2-9b-it)
    
    class Config:
        env_file = ".env" #load variables from file .env
        case_sensitive = False  # Allow case-insensitive env vars
        extra = "ignore"  # Ignore extra fields in .env

settings = Settings() 
