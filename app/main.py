"""Main FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager
import signal
import sys

from app.config import get_settings, validate_settings
from app.utils.logger import setup_logging, get_logger
from app.api.routes import router
from app.services.vector_db import ensure_collection_exists
from app.services.llm import get_ollama_client

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown."""
    # Startup
    logger.info("Starting up application...")
    
    try:
        # Validate settings
        validate_settings()
        logger.info("Settings validated")
        
        # Initialize vector database
        ensure_collection_exists()
        logger.info("Vector database initialized")
        
        # Check Ollama connection
        ollama_client = get_ollama_client()
        if ollama_client.check_health():
            logger.info("Ollama connection successful")
        else:
            logger.warning("Ollama connection failed - LLM features may not work")
        
        logger.info("Application startup complete")
        
    except Exception as e:
        logger.error(f"Startup error: {e}")
        sys.exit(1)
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    logger.info("Application shutdown complete")


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    settings = get_settings()
    
    # Setup logging
    setup_logging()
    
    # Create app
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Production-ready multilingual agentic RAG system",
        lifespan=lifespan
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )
    
    # Add rate limiting
    if settings.rate_limit_enabled:
        limiter = Limiter(key_func=get_remote_address)
        app.state.limiter = limiter
        app.add_exception_handler(RateLimitExceeded, lambda request, exc: {
            "detail": "Rate limit exceeded"
        })
    
    # Include routes
    app.include_router(router)
    
    # Root endpoint
    @app.get("/")
    async def root():
        """Root endpoint."""
        return {
            "name": settings.app_name,
            "version": settings.app_version,
            "status": "running",
            "docs": "/docs"
        }
    
    return app


# Create app instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    settings = get_settings()
    
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        workers=settings.api_workers,
        reload=settings.api_reload,
        log_level=settings.log_level.lower()
    )

