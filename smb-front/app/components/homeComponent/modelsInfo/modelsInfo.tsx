
import React from 'react';
import './ModelsInfo.css';
import ModelGrid from "~/components/homeComponent/modelsInfo/modelGrid";
import ModelController from "~/components/homeComponent/modelsInfo/modelController";

interface Model {
    id: string;
    name: string;
    description: string;
    useCase: string;
    selected: boolean;
}


interface ModelsInfoProps {
    models: Model[];
    setModels: (value: (((prevState: Model[]) => Model[]) | Model[])) => void;
}


const ModelsInfo: React.FC<ModelsInfoProps> = ({models, setModels}) => {

    const toggleModel = (id: string) => {
        setModels(models.map(model =>
            model.id === id ? { ...model, selected: !model.selected } : model
        ));
    };

    const selectedModelsCount = models.filter(m => m.selected).length;

    return (
        <section className="models-info">
            <h2>Модели анализа</h2>
            <p className="section-description">
                Выберите модели для анализа. Рекомендуем использовать все для максимальной точности.
                <span className="selected-count"> Выбрано: {selectedModelsCount}/4</span>
            </p>

            <ModelGrid
                models={models}
                toggleModel={toggleModel}
            />

            <ModelController
                models={models}
                setModels={setModels}
            />
        </section>
    );
};

export default ModelsInfo;