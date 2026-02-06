from fastapi import FastAPI
from app.api.routes import auth, user, mail, template, group
from app.api.middleware.ratelimit import RateLimitMiddleware

def create_app() -> FastAPI:
    app = FastAPI(title="CorpoMailer API")
    
    app.add_middleware(RateLimitMiddleware)
    
    app.include_router(auth.router, prefix="/auth", tags=["auth"])
    app.include_router(user.router, prefix="/users", tags=["users"])
    app.include_router(mail.router, prefix="/mail", tags=["mail"])
    app.include_router(template.router, prefix="/templates", tags=["templates"])
    app.include_router(group.router, prefix="/groups", tags=["groups"])
    
    return app

app = create_app()
