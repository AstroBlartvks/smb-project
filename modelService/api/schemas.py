"""Pydantic модели для валидации запросов/ответов"""
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime


class PredictionRequest(BaseModel):
    """Модель запроса для прогнозирования банкротства"""

    # Financial metrics
    revenue: float = Field(..., description="Выручка (руб.)", gt=0)
    net_profit: float = Field(..., description="Чистая прибыль (руб.)")
    total_assets: float = Field(..., description="Активы (руб.)", gt=0)
    total_liabilities: float = Field(..., description="Обязательства (руб.)", ge=0)
    current_assets: float = Field(..., description="Оборотные активы (руб.)", ge=0)
    current_liabilities: float = Field(..., description="Текущие обязательства (руб.)", ge=0)
    equity: float = Field(..., description="Собственный капитал (руб.)")

    # Company metadata
    region: str = Field(..., description="Регион")
    industry: str = Field(..., description="Отрасль")
    company_age: int = Field(..., description="Возраст компании (годы)", ge=0)
    authorized_capital: float = Field(..., description="Уставной капитал (руб.)", gt=0)

    class Config:
        json_schema_extra = {
            "example": {
                "revenue": 15000000.0,
                "net_profit": 500000.0,
                "total_assets": 10000000.0,
                "total_liabilities": 6000000.0,
                "current_assets": 5000000.0,
                "current_liabilities": 3000000.0,
                "equity": 4000000.0,
                "region": "Москва",
                "industry": "Торговля",
                "company_age": 5,
                "authorized_capital": 100000.0
            }
        }


class ModelPrediction(BaseModel):
    """Прогноз отдельной модели"""
    xgboost: float = Field(..., description="XGBoost prediction (0-1)")
    tabnet: float = Field(..., description="TabNet prediction (0-1)")
    simple_nn: float = Field(..., description="SimpleNN prediction (0-1)")
    ensemble: float = Field(..., description="Ensemble prediction (0-1)")


class PredictionResponse(BaseModel):
    """Модель ответа для прогнозирования банкротства"""
    bankruptcy_probability: float = Field(..., description="Вероятность банкротства (0-100%)")
    risk_level: str = Field(..., description="Уровень риска: low, medium, high")
    model_predictions: ModelPrediction
    timestamp: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "bankruptcy_probability": 45.5,
                "risk_level": "medium",
                "model_predictions": {
                    "xgboost": 0.42,
                    "tabnet": 0.48,
                    "simple_nn": 0.46,
                    "ensemble": 0.455
                },
                "timestamp": "2024-01-27T12:00:00"
            }
        }


class FeatureImportance(BaseModel):
    """Важность признака для SHAP объяснения"""
    feature_name: str
    importance: float
    direction: str = Field(..., description="positive or negative")


class ExplanationResponse(BaseModel):
    """Модель ответа для SHAP объяснений"""
    top_features: List[FeatureImportance] = Field(..., description="Топ-10 факторов риска")
    shap_values: Dict[str, float] = Field(..., description="SHAP values для всех признаков")

    class Config:
        json_schema_extra = {
            "example": {
                "top_features": [
                    {
                        "feature_name": "debt_ratio",
                        "importance": 0.25,
                        "direction": "positive"
                    },
                    {
                        "feature_name": "current_ratio",
                        "importance": 0.18,
                        "direction": "negative"
                    }
                ],
                "shap_values": {
                    "debt_ratio": 0.25,
                    "current_ratio": -0.18
                }
            }
        }


class HealthResponse(BaseModel):
    status: str
    version: str
    models_loaded: bool
    timestamp: datetime


class CourtCaseRequest(BaseModel):
    court_data: str = Field(..., description="Court case text data")


class CourtCaseAnalysis(BaseModel):
    analysis: str
    risk_factors: List[str]
    severity: str


class ComprehensiveAnalysisRequest(BaseModel):
    revenue: float
    net_profit: float
    total_assets: float
    total_liabilities: float
    current_assets: float
    current_liabilities: float
    equity: float
    region: str
    industry: str
    company_age: int
    authorized_capital: float
    court_data: Optional[str] = None


class ComprehensiveAnalysisResponse(BaseModel):
    prediction: PredictionResponse
    explanation: ExplanationResponse
    court_analysis: Optional[CourtCaseAnalysis] = None
    ai_summary: str
    timestamp: datetime
