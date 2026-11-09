from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Centralized configuration management for Synapse backend.
    Automatically loads and validates variables from the root .env file.
    """
    # 1. Database Configuration
    DATABASE_URL: str

    # 2. Security & JWT Settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # Default to 7 days

    # 3. Google OAuth Credentials
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str

    # Pydantic v2 configuration to read from the root .env file
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

# Instantiate a global settings object to be imported across the backend
settings = Settings()