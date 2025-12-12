import React from "react";
import type {Model} from "~/components/homeComponent/modelsInfo/models";

interface ModelGridProp {
    models: Model[];
    setModels: (value: (((prevState: Model[]) => Model[]) | Model[])) => void;
}

const ModelController: React.FC<ModelGridProp> = ({models, setModels}) => {
    return (
        <div className="model-controls">
            <button
                className="control-btn select-all"
                onClick={() => setModels(models.map(m => ({ ...m, selected: true })))}
            >
                Выбрать все
            </button>
            <button
                className="control-btn deselect-all"
                onClick={() => setModels(models.map(m => ({ ...m, selected: false })))}
            >
                Снять все
            </button>
        </div>
    )
}

export default ModelController;