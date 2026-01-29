"""Настройки конфигурации для ML сервиса"""
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    """Настройки приложения"""

    APP_NAME: str = "ML Analytics Service"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    BASE_DIR: Path = Path(__file__).parent
    WEIGHTS_DIR: Path = BASE_DIR / "weights"
    DATA_DIR: Path = BASE_DIR / "data"

    XGBOOST_MODEL_PATH: Path = WEIGHTS_DIR / "xgboost_model.pkl"
    TABNET_MODEL_PATH: Path = WEIGHTS_DIR / "tabnet_model.pth"
    SIMPLE_NN_MODEL_PATH: Path = WEIGHTS_DIR / "simple_nn.pth"
    ENSEMBLE_WEIGHTS_PATH: Path = WEIGHTS_DIR / "ensemble_weights.json"

    ENSEMBLE_WEIGHT_XGBOOST: float = 0.4
    ENSEMBLE_WEIGHT_TABNET: float = 0.3
    ENSEMBLE_WEIGHT_SIMPLE_NN: float = 0.3

    NUMERICAL_FEATURES: list = [
        'revenue', 'net_profit', 'total_assets', 'total_liabilities',
        'current_assets', 'current_liabilities', 'equity',
        'current_ratio', 'debt_ratio', 'roe', 'roa', 'profit_margin',
        'company_age', 'authorized_capital'
    ]

    CATEGORICAL_FEATURES: list = ['region', 'industry']

    LOW_RISK_THRESHOLD: float = 0.3
    HIGH_RISK_THRESHOLD: float = 0.7

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

settings.WEIGHTS_DIR.mkdir(parents=True, exist_ok=True)
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
