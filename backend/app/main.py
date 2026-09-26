from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .config import settings
from .database.session import engine, Base, SessionLocal
from .database.models import Buyer
from .demo_data.seed_buyers import seed_demo_database
from .api.buyers import router as buyers_router
from .api.demo import router as demo_router
from .api.health import router as health_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB schema
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # If no buyers exist, seed demo dataset
        count = db.query(Buyer).count()
        if count == 0:
            print("Database empty. Seeding benchmark demo dataset...")
            seed_demo_database(db)
    finally:
        db.close()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Evidence-First B2B Buyer Risk, Entity Resolution, and Payment Behaviour Intelligence Platform for MSMEs.",
    lifespan=lifespan
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix=settings.API_V1_PREFIX)
app.include_router(buyers_router, prefix=settings.API_V1_PREFIX)
app.include_router(demo_router, prefix=settings.API_V1_PREFIX)

@app.get("/")
def root():
    return {
        "message": "Welcome to PS-09-S2 Buyer Intelligence Platform API",
        "docs": "/docs",
        "health": f"{settings.API_V1_PREFIX}/health"
    }
