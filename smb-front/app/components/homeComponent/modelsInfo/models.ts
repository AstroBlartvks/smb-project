export interface Model {
    id: string;
    name: string;
    description: string;
    useCase: string;
    selected: boolean;
}

export const initialModels: Model[] = [
    {
        id: 'xgboost',
        name: 'XGBoost',
        description: 'Градиентный бустинг для табличных данных',
        useCase: 'Анализ финансовых коэффициентов',
        selected: true
    },
    {
        id: 'tabnet',
        name: 'TabNet',
        description: 'Нейросеть с механизмом внимания для табличных данных',
        useCase: 'Финансовые показатели + текстовые признаки',
        selected: true
    },
    {
        id: 'graphsage',
        name: 'GraphSAGE',
        description: 'Графовые нейросети для анализа связей между компаниями',
        useCase: 'Связи с поставщиками, покупателями, аффилированными лицами',
        selected: true
    },
    {
        id: 'tft',
        name: 'TFT',
        description: 'Transformer для анализа временных рядов',
        useCase: 'Исторические данные и тренды',
        selected: true
    }
];
