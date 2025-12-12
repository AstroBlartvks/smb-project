import React from "react";
import type {Model} from "~/components/homeComponent/modelsInfo/models";

interface ModelGridProp {
    models: Model[];
    toggleModel: (id: string) => void;
}

const ModelGrid: React.FC<ModelGridProp> = ({models, toggleModel}) => {
    return (
        <div className="models-grid">
            {models.map((model) => (
                <div
                    key={model.id}
                    className={`model-card ${model.selected ? 'selected' : ''}`}
                    onClick={() => toggleModel(model.id)}
                >
                    <div className="model-header">
                        <h3>{model.name}</h3>
                        <label className="checkbox-container">
                            <input
                                type="checkbox"
                                checked={model.selected}
                                onChange={() => toggleModel(model.id)}
                                onClick={(e) => e.stopPropagation()}
                            />
                            <span className="checkmark"></span>
                        </label>
                    </div>
                    <p className="model-description">{model.description}</p>
                    <div className="model-use-case">
                        <strong>Применение:</strong> {model.useCase}
                    </div>
                </div>
            ))}
        </div>
    )
}

export default ModelGrid;