import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse, Response
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.gzip import GZipMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from database import get_db, engine, Base
from controllers.auth_controller import router as auth_router

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create database tables
try:
    Base.metadata.create_all(bind=engine)
    logger.info("✓ Database tables initialized successfully")
except Exception as e:
    logger.error(f"✗ Failed to initialize database tables: {str(e)}")

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown events"""
    logger.info("🚀 Application startup")
    yield
    logger.info("🛑 Application shutdown")

# Initialize FastAPI app
app = FastAPI(
    title="🔐 User Authentication API",
    description="A modern authentication system with JWT tokens and glass morphism UI",
    version="1.0.0",
    lifespan=lifespan
)

# Security middlewares
logger.info("📦 Configuring security middlewares...")

# Production security middleware
if os.getenv("DEBUG", "False").lower() != "true":
    allowed_hosts = os.getenv("ALLOWED_HOSTS", "*").split(",")
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)
    logger.info(f"✓ Trusted host validation enabled: {allowed_hosts}")

# CORS middleware
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
logger.info(f"✓ CORS enabled for: {allowed_origins}")

# Compression middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
logger.info("✓ GZIP compression enabled")

# Mount static files
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
    logger.info("✓ Static files mounted successfully")
except Exception as e:
    logger.warning(f"⚠ Warning mounting static files: {str(e)}")

# Templates configuration
templates = Jinja2Templates(directory="static")

# Include routers
app.include_router(auth_router, prefix="/api/v1", tags=["authentication"])
logger.info("✓ Authentication routes registered")

# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors"""
    logger.warning(f"Validation error on {request.url}: {exc}")
    return {"detail": exc.errors(), "body": exc.body}

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions"""
    logger.warning(f"HTTP {exc.status_code} on {request.url}: {exc.detail}")
    return {"detail": exc.detail, "status_code": exc.status_code}

# API Routes
@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    """Serve the login/registration page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
def login_page_post(request: Request):
    """Redirect POST to login page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/favicon.ico")
def favicon():
    """Serve favicon"""
    favicon_path = os.path.join("static", "favicon.ico")
    if os.path.exists(favicon_path):
        return FileResponse(favicon_path, media_type="image/x-icon")
    return Response(content=b"", status_code=204, media_type="image/x-icon")

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard_page(request: Request):
    """Serve the dashboard page"""
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/api")
def api_info():
    """API information endpoint"""
    return {
        "name": "User Authentication API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "register": "POST /api/v1/register",
            "login": "POST /api/v1/login",
            "profile": "GET /api/v1/me"
        }
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "auth-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", 8000)),
        log_level=os.getenv("LOG_LEVEL", "info").lower()
    )

