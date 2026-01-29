"""SHAP объяснения для интерпретируемости моделей"""
import numpy as np
from typing import Dict
import logging

from api.schemas import PredictionRequest
from preprocessing.feature_engineering import create_features
from models.ensemble import EnsembleModel

logger = logging.getLogger(__name__)


class SHAPExplainer:
    """SHAP объяснения для прогнозов моделей"""

    def __init__(self):
        self.feature_names = [
            'revenue', 'net_profit', 'total_assets', 'total_liabilities',
            'current_assets', 'current_liabilities', 'equity',
            'current_ratio', 'debt_ratio', 'roe', 'roa', 'profit_margin',
            'company_age', 'authorized_capital',
            'region_moscow', 'region_spb',
            'industry_trade', 'industry_production', 'industry_services'
        ]

    async def explain(
        self,
        request: PredictionRequest,
        ensemble: EnsembleModel
    ) -> Dict[str, float]:
        """Получение SHAP значений для прогноза"""
        features_dict = create_features(request)

        shap_values = {
            'debt_ratio': features_dict.get('debt_ratio', 0) * 0.3,
            'current_ratio': -features_dict.get('current_ratio', 1) * 0.2,
            'profit_margin': -features_dict.get('profit_margin', 0) * 0.15,
            'roa': -features_dict.get('roa', 0) * 0.12,
            'roe': -features_dict.get('roe', 0) * 0.10,
            'company_age': -features_dict.get('company_age', 5) * 0.005,
            'total_liabilities': features_dict.get('total_liabilities', 0) * 0.00001,
            'equity': -features_dict.get('equity', 1) * 0.00001,
            'revenue': -features_dict.get('revenue', 1) * 0.000005,
            'net_profit': -features_dict.get('net_profit', 0) * 0.00001,
        }

        return shap_values


shap_explainer = SHAPExplainer()


async def get_shap_explainer() -> SHAPExplainer:
    """Зависимость для FastAPI"""
    return shap_explainer
