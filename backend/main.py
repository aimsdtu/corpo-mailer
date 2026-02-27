"""FastAPI application entry point"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.db.engine import init_db, close_db
from app.api.main import router as api_router
from app.core.config import get_settings
from app.core.logging import logger, setup_logging
import uvicorn

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan — pool + schema init on startup, teardown on shutdown."""
    setup_logging()
    logger.info("Starting application…")
    try:
        await init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.warning(f"Database initialization skipped: {e}")
        logger.warning("Running in development mode without database")
    yield
    logger.info("Shutting down…")
    try:
        await close_db()
    except Exception as e:
        logger.warning(f"Database cleanup failed: {e}")


app = FastAPI(
    title="DTU Mailing Service API",
    description="API for DTU automated mailing service",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(api_router)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "healthy", "message": "DTU Mailing Service API"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)