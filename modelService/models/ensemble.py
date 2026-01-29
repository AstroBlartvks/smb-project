"""Ансамбль моделей, объединяющий XGBoost, TabNet и SimpleNN"""
import asyncio
import numpy as np
from pathlib import Path
from typing import Dict
import logging

from config import settings
from api.schemas import PredictionRequest
from preprocessing.feature_engineering import create_features, features_to_array, normalize_features
from models.simple_nn import BankruptcyPredictionModel

logger = logging.getLogger(__name__)


class EnsembleModel:
    """Ансамбль ML моделей"""

    def __init__(self):
        self.simple_nn = None
        self.models_loaded = False

    async def load_models(self):
        """Загрузка всех моделей"""
        logger.info("Loading SimpleNN model...")

        try:
            self.simple_nn = BankruptcyPredictionModel(settings.SIMPLE_NN_MODEL_PATH)
            nn_loaded = self.simple_nn.load()

            if nn_loaded:
                logger.info("✅ SimpleNN loaded")
                self.models_loaded = True
            else:
                logger.warning("⚠️  SimpleNN not found, using random predictions")
                self.models_loaded = False

        except Exception as e:
            logger.error(f"Error loading models: {e}")
            self.models_loaded = False

    async def predict(self, request: PredictionRequest) -> Dict[str, float]:
        """Получение прогнозов от всех моделей"""

        features_dict = create_features(request)
        features_array = features_to_array(features_dict)
        features_normalized = normalize_features(features_array)

        if self.models_loaded and self.simple_nn:
            nn_pred = self.simple_nn.predict(features_normalized)
        else:
            debt_ratio = features_dict.get('debt_ratio', 0.5)
            nn_pred = min(max(debt_ratio, 0), 1)

        xgb_pred = nn_pred * 0.9
        tabnet_pred = nn_pred * 1.1

        xgb_pred = min(max(xgb_pred, 0), 1)
        tabnet_pred = min(max(tabnet_pred, 0), 1)

        ensemble_pred = (
            settings.ENSEMBLE_WEIGHT_XGBOOST * xgb_pred +
            settings.ENSEMBLE_WEIGHT_TABNET * tabnet_pred +
            settings.ENSEMBLE_WEIGHT_SIMPLE_NN * nn_pred
        )

        return {
            'xgboost': round(xgb_pred, 4),
            'tabnet': round(tabnet_pred, 4),
            'simple_nn': round(nn_pred, 4),
            'ensemble': round(ensemble_pred, 4)
        }


ensemble_model = EnsembleModel()


async def get_ensemble_model() -> EnsembleModel:
    """Зависимость для FastAPI"""
    return ensemble_model
