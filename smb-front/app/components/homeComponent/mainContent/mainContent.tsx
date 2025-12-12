import React, { useState } from 'react';
import InfoHowItWorks from "~/components/homeComponent/infoHowItWorks/infoHowItWorks";
import DataSources from "~/components/homeComponent/dataSources/DataSources";
import HeroSearch from "~/components/homeComponent/heroSection/heroSearch"
import './MainContent.css';
import {initialModels} from "~/components/homeComponent/modelsInfo/models";

interface Model {
    id: string;
    name: string;
    description: string;
    useCase: string;
    selected: boolean;
}

const MainContent: React.FC = () => {
    const [searchQuery, setSearchQuery] = useState('');
    const [models, setModels] = useState<Model[]>(initialModels);

    const handleSearch = (e: React.FormEvent) => {
        e.preventDefault();
        const activatedModels: Model[] = models.filter((model: Model) => model.selected);

        if (searchQuery.trim()) {
            if (activatedModels.length == 0) {
                alert("Вам будет продемонстрирована только информация из источников! Выберите модель, если хотите получить результат!");
            }

            console.log('Поиск: ', searchQuery.trim());
            console.log(activatedModels);
        } else {
            alert("Введите номер ИНН!");
        }
    };

    return (
        <div className="main-content">
            <HeroSearch
                searchQuery={searchQuery}
                setSearchQuery={setSearchQuery}
                handleSearch={handleSearch}
                models={models}
                setModels={setModels}
            />
            <InfoHowItWorks />
            <DataSources />
        </div>
    );
};

export default MainContent;