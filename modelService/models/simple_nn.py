"""Простая нейронная сеть для прогнозирования банкротства"""
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from pathlib import Path


class BankruptcyNN(nn.Module):
    """Нейронная сеть для прогнозирования банкротства"""

    def __init__(self, input_dim=19):
        super().__init__()

        self.fc1 = nn.Linear(input_dim, 128)
        self.bn1 = nn.BatchNorm1d(128)
        self.dropout1 = nn.Dropout(0.3)

        self.fc2 = nn.Linear(128, 64)
        self.bn2 = nn.BatchNorm1d(64)
        self.dropout2 = nn.Dropout(0.3)

        self.fc3 = nn.Linear(64, 32)
        self.bn3 = nn.BatchNorm1d(32)

        self.fc4 = nn.Linear(32, 1)

    def forward(self, x):
        x = F.relu(self.bn1(self.fc1(x)))
        x = self.dropout1(x)

        x = F.relu(self.bn2(self.fc2(x)))
        x = self.dropout2(x)

        x = F.relu(self.bn3(self.fc3(x)))

        x = torch.sigmoid(self.fc4(x))
        return x


class BankruptcyPredictionModel:
    """Обертка для модели прогнозирования банкротства"""

    def __init__(self, model_path: Path = None):
        self.model = BankruptcyNN(input_dim=19)
        self.model_path = model_path
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)

    def load(self):
        """Загрузка весов модели"""
        if self.model_path and self.model_path.exists():
            self.model.load_state_dict(torch.load(self.model_path, map_location=self.device))
            self.model.eval()
            return True
        return False

    def predict(self, features: np.ndarray) -> float:
        """Прогноз вероятности банкротства"""
        self.model.eval()

        with torch.no_grad():
            x = torch.FloatTensor(features).to(self.device)
            output = self.model(x)
            return output.item()
