"""
Configuration Management
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application settings"""
    
    # Environment
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Database
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///./fabri8.db"
    )
    
    # Redis
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # API Keys
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY environment variable not set!")
    
    # JWT
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Frontend
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    # Servers
    SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT = int(os.getenv("SERVER_PORT", "8000"))
    WS_HOST = os.getenv("WS_HOST", "0.0.0.0")
    WS_PORT = int(os.getenv("WS_PORT", "8001"))
    
    # AI Models
    AGENT_MODELS = {
        "pm": "anthropic/claude-3.5-sonnet",
        "ui": "openai/gpt-4o",
        "frontend": "deepseek/deepseek-coder",
        "backend": "deepseek/deepseek-coder",
        "writer": "google/gemini-2.0-flash-exp:free",
        "reviewer": "anthropic/claude-3.5-sonnet",
        "qa": "google/gemini-pro",
        "debugger": "deepseek/deepseek-coder"
    }
    
    # Workflow Phases
    WORKFLOW_PHASES = {
        1: "Discovery & Planning",
        2: "Design & Architecture",
        3: "Implementation",
        4: "Integration Standup",
        5: "Refinement & Polish",
        6: "Testing & Validation",
        7: "Delivery"
    }
    
    # Rate Limiting
    RATE_LIMIT_CALLS = 100
    RATE_LIMIT_PERIOD = 60  # seconds

settings = Settings()
