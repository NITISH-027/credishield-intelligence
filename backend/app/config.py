import os
from pydantic import BaseModel

class Settings(BaseModel):
    PROJECT_NAME: str = "Buyer Intelligence & Payment Risk Intelligence Platform (PS-09-S2)"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./buyer_intelligence.db")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() in ("true", "1", "t")
    USE_LIVE_PUBLIC_SOURCES: bool = os.getenv("USE_LIVE_PUBLIC_SOURCES", "False").lower() in ("true", "1", "t")
    MODEL_ARTIFACTS_DIR: str = os.getenv("MODEL_ARTIFACTS_DIR", "backend/app/ml/models")

settings = Settings()
