from app.models import Base
from app.database import engine
from app.config import settings
from app.routes import auth, users
from app.database import get_db


import uvicorn
import logging
from datetime import datetime, timezone
from sqlalchemy import text
from typing import Annotated
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from fastapi.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startapp
    logger.info("Starting up...")

    # Create database tables
    Base.metadata.create_all(bind=engine)

    # initialize OAuth
    from app.auth import oauth
    from starlette.config import Config
    config = Config('.env')
    oauth.register(
        name='google',
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret = settings.GOOGLE_CLIENT_SECRET,
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'}
    )
    app.state.oauth = oauth
    
    yield

    # shutdown
    logger.info("Shutting down...")

middleware = [
    Middleware(
        SessionMiddleware,
        secret_key=settings.SECRET_KEY,
        session_cookie="autho_session",
        max_age=14*24*60*60, # 14 days in seconds
        same_site="lax",
        https_only=False if settings.ENVIRONMENT == "development" else True
    ),
]

app = FastAPI(
    title="Autho API",
    description="Secure Authentication API with Google and Apple Sign-in",
    version="1.0.0",
    lifespan=lifespan,
    middleware=middleware
)

# security headers middleware
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policty"] = "default-src 'self'"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    return response

# add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# add trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"] if settings.ENVIRONMENT == "development" else ["http://localhost:3000"]
)

# add GZip middleware for performance
app.add_middleware(GZipMiddleware, minimum_size=1000)

# redirect HTTP to HTTPS in production
if settings.ENVIRONMENT == "production":
    app.add_middleware(HTTPSRedirectMiddleware)

app.include_router(auth.router)
app.include_router(users.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to Auth0 API",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    # healh check endpoint
    try:
        # check database connection
        result = db.execute(text("SELECT 1"))
        result.fetchone() # execute the query
        return {
            "status": "healthy",
            "database": "connected",
            "environment": settings.ENVIRONMENT,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Service unhealthy: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development"
    )



