"""Инженерия признаков для прогнозирования банкротства"""
import pandas as pd
import numpy as np
from typing import Dict, Any
from api.schemas import PredictionRequest


def calculate_financial_ratios(data: Dict[str, Any]) -> Dict[str, float]:
    """Расчет финансовых коэффициентов из сырых финансовых данных"""

    revenue = data.get('revenue', 0)
    net_profit = data.get('net_profit', 0)
    total_assets = data.get('total_assets', 1)
    total_liabilities = data.get('total_liabilities', 0)
    current_assets = data.get('current_assets', 0)
    current_liabilities = data.get('current_liabilities', 1)
    equity = data.get('equity', 1)

    ratios = {
        'current_ratio': current_assets / current_liabilities if current_liabilities > 0 else 0,
        'debt_ratio': total_liabilities / total_assets if total_assets > 0 else 0,
        'roe': net_profit / equity if equity > 0 else 0,
        'roa': net_profit / total_assets if total_assets > 0 else 0,
        'profit_margin': net_profit / revenue if revenue > 0 else 0,
    }

    return ratios


def create_features(request: PredictionRequest) -> Dict[str, float]:
    """Создание вектора признаков из запроса на прогноз"""
    data = request.model_dump()

    ratios = calculate_financial_ratios(data)

    features = {
        'revenue': data['revenue'],
        'net_profit': data['net_profit'],
        'total_assets': data['total_assets'],
        'total_liabilities': data['total_liabilities'],
        'current_assets': data['current_assets'],
        'current_liabilities': data['current_liabilities'],
        'equity': data['equity'],

        'current_ratio': ratios['current_ratio'],
        'debt_ratio': ratios['debt_ratio'],
        'roe': ratios['roe'],
        'roa': ratios['roa'],
        'profit_margin': ratios['profit_margin'],

        'company_age': data['company_age'],
        'authorized_capital': data['authorized_capital'],

        'region_moscow': 1 if data['region'].lower() == 'москва' else 0,
        'region_spb': 1 if 'спб' in data['region'].lower() or 'петербург' in data['region'].lower() else 0,

        'industry_trade': 1 if 'торг' in data['industry'].lower() else 0,
        'industry_production': 1 if 'произ' in data['industry'].lower() else 0,
        'industry_services': 1 if 'услуг' in data['industry'].lower() else 0,
    }

    return features


def features_to_array(features: Dict[str, float]) -> np.ndarray:
    """Преобразование словаря признаков в numpy массив в фиксированном порядке"""

    feature_order = [
        'revenue', 'net_profit', 'total_assets', 'total_liabilities',
        'current_assets', 'current_liabilities', 'equity',
        'current_ratio', 'debt_ratio', 'roe', 'roa', 'profit_margin',
        'company_age', 'authorized_capital',
        'region_moscow', 'region_spb',
        'industry_trade', 'industry_production', 'industry_services'
    ]

    return np.array([features.get(f, 0) for f in feature_order]).reshape(1, -1)


def normalize_features(features: np.ndarray) -> np.ndarray:
    """Нормализация признаков"""
    features = np.clip(features, -1e10, 1e10)

    features[:, :14] = np.log1p(np.abs(features[:, :14])) * np.sign(features[:, :14])

    return features
