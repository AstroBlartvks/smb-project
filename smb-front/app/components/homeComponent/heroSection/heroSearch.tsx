import React from "react";
import SearchForm from "~/components/search/SearchForm";
import ModelsInfo from "~/components/homeComponent/modelsInfo/modelsInfo";

interface heroSearchFormProp {
    searchQuery: string;
    setSearchQuery: (value: string | ((prevState: string) => string)) => void;
    handleSearch: (e: React.FormEvent) => void;
}

const HeroSearch: React.FC<heroSearchFormProp> = ({ searchQuery, setSearchQuery, handleSearch }) => {
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
                    <ModelsInfo />
                </div>
            </div>
        </section>
    )
}

export default HeroSearch;