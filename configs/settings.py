from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "LLM-Production-Pipeline"
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1"
    
    # LLM Settings
    LLM_PROVIDER: str = "mock" # Changed to mock by default for demonstration
    GEMINI_API_KEY: Optional[str] = None
    MODEL_NAME: str = "gemini-1.5-flash"
    
    # Monitoring
    PROMETHEUS_METRICS: bool = True
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

settings = Settings()
