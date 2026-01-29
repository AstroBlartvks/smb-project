"""Генерация синтетических данных для быстрого тестирования"""
import pandas as pd
import numpy as np
from pathlib import Path

np.random.seed(42)


def generate_synthetic_data(n_samples=1000):
    """Генерация синтетических данных для обучения моделей"""

    data = []

    for i in range(n_samples):
        is_bankrupt = np.random.rand() > 0.5

        if is_bankrupt:
            revenue = np.random.uniform(100000, 5000000)
            net_profit = np.random.uniform(-revenue * 0.5, revenue * 0.05)
            total_assets = np.random.uniform(revenue * 0.3, revenue * 2)
            total_liabilities = np.random.uniform(total_assets * 0.7, total_assets * 1.2)
            current_assets = total_assets * np.random.uniform(0.2, 0.5)
            current_liabilities = total_liabilities * np.random.uniform(0.5, 0.9)
            equity = total_assets - total_liabilities
            company_age = np.random.randint(1, 15)
            authorized_capital = np.random.uniform(10000, 200000)
        else:
            revenue = np.random.uniform(500000, 50000000)
            net_profit = np.random.uniform(revenue * 0.05, revenue * 0.25)
            total_assets = np.random.uniform(revenue * 0.5, revenue * 3)
            total_liabilities = np.random.uniform(total_assets * 0.2, total_assets * 0.6)
            current_assets = total_assets * np.random.uniform(0.4, 0.7)
            current_liabilities = total_liabilities * np.random.uniform(0.3, 0.6)
            equity = total_assets - total_liabilities
            company_age = np.random.randint(3, 25)
            authorized_capital = np.random.uniform(50000, 1000000)

        regions = ['Moscow', 'SPB', 'Moscow_region', 'Novosibirsk', 'Ekaterinburg']
        industries = ['Trade', 'Manufacturing', 'Services', 'IT', 'Construction']

        data.append({
            'inn': f'{i:010d}',
            'revenue': max(revenue, 0),
            'net_profit': net_profit,
            'total_assets': max(total_assets, 1),
            'total_liabilities': max(total_liabilities, 0),
            'current_assets': max(current_assets, 0),
            'current_liabilities': max(current_liabilities, 1),
            'equity': equity,
            'region': np.random.choice(regions),
            'industry': np.random.choice(industries),
            'company_age': company_age,
            'authorized_capital': max(authorized_capital, 10000),
            'is_bankrupt': int(is_bankrupt)
        })

    return pd.DataFrame(data)


if __name__ == "__main__":
    print("Генерация синтетических данных...")

    df = generate_synthetic_data(n_samples=1000)

    output_path = Path(__file__).parent.parent / "data" / "raw" / "companies_data.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    print(f"[OK] Сохранено {len(df)} образцов в {output_path}")
    print(f"\nРаспределение классов:")
    print(df['is_bankrupt'].value_counts())
    print(f"\nПервые несколько строк:")
    print(df.head())
