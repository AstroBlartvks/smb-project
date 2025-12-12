import React from "react";
import SearchForm from "~/components/search/SearchForm";
import ModelsInfo from "~/components/homeComponent/modelsInfo/modelsInfo";
import type {Model} from "~/components/homeComponent/modelsInfo/models";

interface heroSearchFormProp {
    searchQuery: string;
    setSearchQuery: (value: string | ((prevState: string) => string)) => void;
    handleSearch: (e: React.FormEvent) => void;
    models: Model[];
    setModels: (value: (((prevState: Model[]) => Model[]) | Model[])) => void;
}

const HeroSearch: React.FC<heroSearchFormProp> = ({ searchQuery, setSearchQuery, handleSearch, models, setModels }) => {
    return (
        <section className="hero-section">
            <div className="hero-content">
                <h1 className="hero-title">
                    Прогнозирование банкротств МСБ
                </h1>
                <p className="hero-subtitle">
                    Анализ рисков на основе финансовых показателей, новостей и связей компаний
                </p>

                <div className="hero-search-container">
                    <SearchForm
                        searchQuery={searchQuery}
                        setSearchQuery={setSearchQuery}
                        handleSearch={handleSearch}
                    />
                    <ModelsInfo
                        models={models}
                        setModels={setModels}
                    />
                </div>
            </div>
        </section>
    )
}

export default HeroSearch;