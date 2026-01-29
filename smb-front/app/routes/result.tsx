import {useLocation, useNavigate} from "react-router";
import React, { useState, useEffect } from 'react';
import Header from "~/components/header/Header";
import './ResultPage.css'

interface ResultState {
    results: any;
    query: string;
}

interface CompanyData {
    [key: string]: string;
}

const ResultPage: React.FC = () => {
    const location = useLocation();
    const state = location.state as ResultState;
    const navigate = useNavigate();
    const [companyData, setCompanyData] = useState<CompanyData>({});
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (state?.results) {
            try {
                let parsedData;
                if (typeof state.results === 'string') {
                    parsedData = JSON.parse(state.results);
                    if (parsedData.text) {
                        parsedData = JSON.parse(parsedData.text);
                    }
                } else {
                    parsedData = state.results;
                    if (parsedData.text) {
                        parsedData = JSON.parse(parsedData.text);
                    }
                }
                setCompanyData(parsedData);
            } catch (error) {
                console.log(state.results);
                console.error('Ошибка парсинга данных:', error);
                setCompanyData({});
            }
            setLoading(false);
        }
    }, [state]);

    if (!companyData) {
        return <div>No data available</div>;
    }

    const parsedData = typeof companyData === 'string' ? JSON.parse(companyData) : companyData;
    const inn = state.query.replace(" ", "").replace("%20", "");

    const handleDetailedAnalysis = () => {
        console.log(inn.replace(" ", ""));
        navigate(`/analysis/${inn}`);
    };

    return (
        <>
            <Header/>
            <div className="result-container">
                <h1>Company Information</h1>
                <pre>{JSON.stringify(parsedData, null, 2)}</pre>

                {inn && (
                    <button onClick={handleDetailedAnalysis} className="detailed-analysis-btn">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M9 11l3 3L22 4"/>
                            <path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11"/>
                        </svg>
                        Detailed ML Analysis
                    </button>
                )}
            </div>
        </>
    );
}


export default ResultPage;