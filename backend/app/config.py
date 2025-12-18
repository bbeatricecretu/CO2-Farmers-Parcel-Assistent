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
    LLM_MODEL: str = "gemma-3-12b"  # Default model, can be overridden in .env (e.g., gemma-2-9b-it)
    
    # Messaging Configuration
    MESSAGING_PROVIDER: str = "mock"  # Options: "twilio", "meta", "mock"
    
    # Twilio Configuration (for WhatsApp)
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_PHONE_NUMBER: Optional[str] = None  # Twilio WhatsApp number (e.g., +14155238886)
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )

settings = Settings() 
