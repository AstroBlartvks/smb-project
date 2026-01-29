"""Эндпоинт проверки здоровья"""
from fastapi import APIRouter
from datetime import datetime
from api.schemas import HealthResponse
from config import settings

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Эндпоинт проверки здоровья сервиса"""
    models_loaded = True

    return HealthResponse(
        status="healthy",
        version=settings.APP_VERSION,
        models_loaded=models_loaded,
        timestamp=datetime.now()
    )
