"""FastAPI application entry point"""
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from app.db.session import get_database, close_database
from app.api.services.userservice import UserService
from app.api.models.user import UserCreate, UserResponse
from app.db.session import get_db_session
from app.db.protocol import Database
from dotenv import load_dotenv
load_dotenv()


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


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "healthy", "message": "DTU Mailing Service API"}


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "connected"
    }


@app.post("/users", response_model=UserResponse)
async def create_user(
    user_create: UserCreate,
    db: Database = Depends(get_db_session)
):
    """Create a new user"""
    service = UserService(db)
    user = await service.create_user(user_create)
    return user


@app.get("/users/{uuid}", response_model=UserResponse)
async def get_user(
    uuid: str,
    db: Database = Depends(get_db_session)
):
    """Get user by UUID"""
    from uuid import UUID
    service = UserService(db)
    user = await service.get_user_by_uuid(UUID(uuid))
    if not user:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="User not found")
    return user


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)