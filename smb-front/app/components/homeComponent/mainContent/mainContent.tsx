import React, { useState } from 'react';
import InfoHowItWorks from "~/components/homeComponent/infoHowItWorks/infoHowItWorks";
import DataSources from "~/components/homeComponent/dataSources/DataSources";
import HeroSearch from "~/components/homeComponent/heroSection/heroSearch"
import './MainContent.css';

interface MainContentProps {
    onSearch?: (query: string) => void;
}

const MainContent: React.FC<MainContentProps> = ({ onSearch }) => {
    const [searchQuery, setSearchQuery] = useState('');

    const handleSearch = (e: React.FormEvent) => {
        e.preventDefault();
        if (onSearch && searchQuery.trim()) {
            onSearch(searchQuery.trim());
        }
    };

    return (
        <div className="main-content">
            <HeroSearch
                searchQuery={searchQuery}
                setSearchQuery={setSearchQuery}
                handleSearch={handleSearch}
            />
            <InfoHowItWorks />
            <DataSources />
        </div>
    );
};

export default MainContent;