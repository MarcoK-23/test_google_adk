"""
Configuration settings for Support Squad Backend
"""

import os
from typing import Optional

class Settings:
    """Application settings"""
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    
    # Google Cloud Configuration (for production)
    GOOGLE_CLOUD_PROJECT_ID: Optional[str] = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    GOOGLE_CLOUD_LOCATION: str = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    
    # Chatwoot Configuration
    CHATWOOT_WEBHOOK_SECRET: Optional[str] = os.getenv("CHATWOOT_WEBHOOK_SECRET")
    CHATWOOT_ACCOUNT_ID: Optional[str] = os.getenv("CHATWOOT_ACCOUNT_ID")
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "text")
    
    # Security Configuration (for production)
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    ALLOWED_HOSTS: list = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    
    # Database Configuration (for future use)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./support_squad.db")
    
    # ADK Configuration
    ADK_MODEL_NAME: str = os.getenv("ADK_MODEL_NAME", "mock-adk-model")
    ADK_ENDPOINT: Optional[str] = os.getenv("ADK_ENDPOINT")
    
    # Application Configuration
    APP_NAME: str = "Support Squad Backend"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "FastAPI backend for Chatwoot integration with Google ADK"

# Global settings instance
settings = Settings()

def get_settings() -> Settings:
    """Get application settings"""
    return settings 