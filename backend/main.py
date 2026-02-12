"""FastAPI application entry point"""
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.session import get_database, close_database
from app.api.main import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan"""
    # Startup
    print("🚀 Starting application...")
    await get_database()
    yield
    # Shutdown
    print("🛑 Shutting down application...")
    await close_database()


app = FastAPI(
    title="DTU Mailing Service API",
    description="API for DTU automated mailing service",
    version="1.0.0",
    lifespan=lifespan
)

# Include API routes
app.include_router(api_router)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "healthy", "message": "DTU Mailing Service API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)