from fastapi import APIRouter
from ..config import settings

router = APIRouter(tags=["Health"])

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "mode": "DEMO_BENCHMARK" if not settings.USE_LIVE_PUBLIC_SOURCES else "LIVE_CONNECTORS"
    }
