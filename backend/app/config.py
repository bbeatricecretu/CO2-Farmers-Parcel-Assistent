from pydantic_settings import BaseSettings, SettingsConfigDict
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
    LLM_MODEL: str = "gemini-2.5-flash-lite"  # Default model, can be overridden in .env (e.g., gemma-2-9b-it)
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )

settings = Settings() 
