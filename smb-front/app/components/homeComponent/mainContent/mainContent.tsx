import React, { useState } from 'react';
import axios from 'axios';
import InfoHowItWorks from "~/components/homeComponent/infoHowItWorks/infoHowItWorks";
import DataSources from "~/components/homeComponent/dataSources/DataSources";
import HeroSearch from "~/components/homeComponent/heroSection/heroSearch"
import {initialModels} from "~/components/homeComponent/modelsInfo/models";
import './MainContent.css';

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
    const api = axios.create({
        baseURL: import.meta.env.VITE_API_URL || '/api/',
        timeout: 10000
    });

    const handleSearch = async (e: React.FormEvent) => {
        e.preventDefault();

        if (searchQuery.length != 12) {
            alert("Длина ИНН юридического лица должна быть 10 цифр!");
            return;
        }

        try {
            const toSendData = {
                TaxpayerIdentificationNumber: searchQuery,
                models: models.filter(m => m.selected).map(m => m.id)
            }

            const { data } = await api.post('/search', toSendData);

            console.log(data);

        } catch (error) {
            if (axios.isAxiosError(error)) {
                alert(`Ошибка: ${error.response?.data?.message || error.message}`);
            }
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