import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router';
import Header from "~/components/header/Header";
import './ResultPage.css';

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
                console.error('Ошибка парсинга данных:', error);
                setCompanyData({});
            }
            setLoading(false);
        }
    }, [state]);

    if (!state) {
        return (
            <div className="home-page">
                <Header />
                <div className="no-data">
                    <h2>Нет данных для отображения</h2>
                    <p>Пожалуйста, выполните поиск для получения информации о компании</p>
                </div>
            </div>
        );
    }

    const { query } = state;

    const fieldOrder = [
        'Сокращённое наименование',
        'Полное наименование',
        'Дата регистрации',
        'Статус',
        'Статус по ЕГРЮЛ',
        'Регион',
        'Уставный капитал'
    ];

    const sortedFields = fieldOrder
        .filter(field => companyData[field])
        .map(field => ({
            key: field,
            value: companyData[field]
        }));

    return (
        <div className="home-page">
            <Header />

            <div className="result-container">
                <div className="result-header">
                    <h1 className="result-title">Результаты поиска</h1>
                    <div className="result-query">
                        <span className="query-label">ИНН компании:</span>
                        <span className="query-value">{query}</span>
                    </div>
                </div>

                {loading ? (
                    <div className="loading-container">
                        <div className="loading-spinner"></div>
                        <p>Загрузка данных...</p>
                    </div>
                ) : sortedFields.length > 0 ? (
                    <div className="company-info-card">
                        <div className="company-info-header">
                            <h2 className="company-name">
                                {companyData['Сокращённое наименование'] ||
                                    companyData['Полное наименование'] ||
                                    'Информация о компании'}
                            </h2>
                            {companyData['Статус'] && (
                                <span className={`status-badge ${companyData['Статус'].includes('Действует') ? 'status-active' : 'status-inactive'}`}>
                                    {companyData['Статус']}
                                </span>
                            )}
                        </div>

                        <div className="company-info-table">
                            {sortedFields.map((field, index) => (
                                <div key={field.key} className={`info-row ${index % 2 === 0 ? 'even' : 'odd'}`}>
                                    <div className="info-label">{field.key}</div>
                                    <div className="info-value">{field.value}</div>
                                </div>
                            ))}
                        </div>

                        <div className="company-info-footer">
                            <div className="info-note">
                                <span>Данные актуальны на момент запроса</span>
                            </div>
                        </div>
                    </div>
                ) : (
                    <div className="error-message">
                        <h3>Не удалось загрузить данные о компании</h3>
                        <p>Попробуйте выполнить поиск еще раз или проверьте корректность введенного ИНН</p>
                    </div>
                )}

                <div className="result-actions">
                    <button
                        className="back-button"
                        onClick={() => window.history.back()}
                    >
                        ← Вернуться к поиску
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ResultPage;