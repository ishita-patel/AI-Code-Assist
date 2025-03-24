from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    DATABASE_URL: str = "sqlite:///./code.db"  # Default SQLite URL

    class Config:
        env_file = ".env"  # Load environment variables from .env file

# Create an instance of Settings
settings = Settings()