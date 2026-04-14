import psutil
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from loguru import logger

from configs.settings import settings
from utils.logger_config import setup_logging
from app.routes import inference, monitoring

# Initialize logging
setup_logging()

# Rate limiting setup
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(
    title=settings.APP_NAME,
    description="Refined MLOps Pipeline for Production LLM Deployment",
    version="2.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Register Routes
app.include_router(inference.router, prefix="/api/v1", tags=["Inference"])
app.include_router(monitoring.router, prefix="/api/v1", tags=["Monitoring"])

@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "healthy",
        "resources": {
            "cpu": f"{psutil.cpu_percent()}%",
            "memory": f"{psutil.virtual_memory().percent}%"
        }
    }

@app.get("/api/v1/logs", tags=["Monitoring"])
async def get_logs(limit: int = 50):
    """Retrieves recent logs for the dashboard viewer efficiently."""
    try:
        # Use a more memory-efficient way to get last lines
        import collections
        with open("logs/app.log", "r", encoding="utf-8") as f:
            return {"logs": list(collections.deque(f, maxlen=limit))}
    except FileNotFoundError:
        return {"logs": ["Log file not found."]}

if __name__ == "__main__":
    import uvicorn
    # Optimized for high concurrency
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=8000, 
        workers=1, # Shared state requires 1 worker for in-memory tracking
        loop="auto", 
        http="auto",
        log_level="info"
    )
