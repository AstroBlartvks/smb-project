"""ML сервис аналитики - FastAPI приложение"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from api.routes import predict, explain, health, analyze
from config import settings
from models.ensemble import ensemble_model
from models.qwen_model import qwen_model
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load models on startup, cleanup on shutdown"""
    logger.info("=Starting ML Analytics Service...")

    try:
        # Load models
        logger.info("Loading ML models...")
        await ensemble_model.load_models()
        logger.info(" Models loaded successfully!")
    except Exception as e:
        logger.error(f"L Failed to load models: {e}")
        logger.warning("Service will start but predictions will fail")

    yield

    logger.info("=Shutting down ML Analytics Service...")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Bankruptcy prediction service using ensemble of ML models",
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/ml", tags=["Health"])
app.include_router(predict.router, prefix="/api/ml", tags=["Prediction"])
app.include_router(explain.router, prefix="/api/ml", tags=["Explanation"])
app.include_router(analyze.router, prefix="/api/ml", tags=["Analysis"])


@app.get("/", tags=["Root"])
async def root():
    """Корневой эндпоинт"""
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs"
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
