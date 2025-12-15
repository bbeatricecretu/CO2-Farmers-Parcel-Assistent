from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./farmers_db.sqlite"
    
    class Config:
        env_file = ".env" #load variables from file .env

settings = Settings() 
