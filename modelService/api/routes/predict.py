"""Эндпоинты прогнозирования"""
from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from api.schemas import PredictionRequest, PredictionResponse, ModelPrediction
from config import settings
from models.ensemble import get_ensemble_model, EnsembleModel

router = APIRouter()


def get_risk_level(probability: float) -> str:
    """Определение уровня риска на основе вероятности"""
    if probability < settings.LOW_RISK_THRESHOLD:
        return "low"
    elif probability < settings.HIGH_RISK_THRESHOLD:
        return "medium"
    else:
        return "high"


@router.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict_bankruptcy(
    request: PredictionRequest,
    ensemble: EnsembleModel = Depends(get_ensemble_model)
):
    """Прогноз вероятности банкротства для компании"""
    try:
        predictions = await ensemble.predict(request)

        bankruptcy_prob = predictions['ensemble'] * 100

        response = PredictionResponse(
            bankruptcy_probability=round(bankruptcy_prob, 2),
            risk_level=get_risk_level(predictions['ensemble']),
            model_predictions=ModelPrediction(**predictions),
            timestamp=datetime.now()
        )

        return response

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )
