import { useParams, useNavigate } from 'react-router';
import { useState, useEffect } from 'react';
import axios from 'axios';
import Header from '~/components/header/Header';
import './AnalysisPage.css';

interface ModelPredictions {
  xgboost: number;
  tabnet: number;
  simple_nn: number;  
  ensemble: number;
}

interface FeatureImportance {
  feature_name: string; 
  importance: number;
  direction: string;
}

interface Prediction {
  bankruptcy_probability: number; 
  risk_level: string; 
  model_predictions: ModelPredictions;  
  timestamp: string;
}

interface Explanation {
  top_features: FeatureImportance[];  
  shap_values: Record<string, number>;  
}

interface CourtAnalysis {
  analysis: string;
  risk_factors: string[];  
  severity: string;
}

interface AnalysisData {
  companyInfo: Record<string, any>;
  analysis: {
    prediction: Prediction;
    explanation: Explanation;
    court_analysis: CourtAnalysis | null;  
    ai_summary: string; 
    timestamp: string;
  };
}

export default function AnalysisPage() {
  const { inn } = useParams();
  const navigate = useNavigate();
  const [analysisData, setAnalysisData] = useState<AnalysisData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAnalysis = async () => {
      try {
        const api = await axios.create({
          baseURL: import.meta.env.VITE_API_URL || '/api/',
          timeout: 10000
        });

        const response = await api.post(`/analysis/${inn}`);
        console.log(response.data);

        setAnalysisData(response.data);
      } catch (err) {
        setError('Failed to load analysis');
        console.error('Analysis error:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchAnalysis();
  }, [inn]);

  if (loading) {
    return (
      <div className="analysis-page">
        <Header />
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Анализируем компанию...</p>
        </div>
      </div>
    );
  }

  if (error || !analysisData) {
    return (
      <div className="analysis-page">
        <Header />
        <div className="error-message">
          <p>{error || 'No data available'}</p>
          <button onClick={() => navigate('/')}>Back to Home</button>
        </div>
      </div>
    );
  }

  const { companyInfo, analysis } = analysisData;
  const { prediction, explanation, court_analysis, ai_summary } = analysis;

  const getRiskColor = () => {
    if (prediction.bankruptcy_probability < 30) return '#10b981';
    if (prediction.bankruptcy_probability < 70) return '#f59e0b';
    return '#ef4444';
  };

  return (
    <div className="analysis-page">
      <Header />

      <div className="analysis-container">
        <button className="back-button" onClick={() => navigate('/result', { state: { companyData: companyInfo } })}>
          ← Back
        </button>

        <h1>Анализ вероятности банкротсва</h1>

        <div className="company-header">
          <h2>{companyInfo['Сокращенное наименование'] || companyInfo['name'] || 'Компания'}</h2>
          <p>ИНН: {inn}</p>
        </div>

        <div className="risk-gauge-section">
          <div className="risk-gauge">
            <svg width="300" height="200" viewBox="0 0 300 200">
              <path
                d="M 30 150 A 120 120 0 0 1 270 150"
                fill="none"
                stroke="#e5e7eb"
                strokeWidth="20"
              />
              <path
                d="M 30 150 A 120 120 0 0 1 270 150"
                fill="none"
                stroke={getRiskColor()}
                strokeWidth="20"
                strokeDasharray={`${prediction.bankruptcy_probability * 3.77} 377`}
              />
              <text x="150" y="120" textAnchor="middle" fontSize="48" fontWeight="bold" fill={getRiskColor()}>
                {prediction?.bankruptcy_probability?.toFixed(1) ?? '0.0'}%
              </text>
              <text x="150" y="150" textAnchor="middle" fontSize="16" fill="#6b7280">
                Вероятность банкротства
              </text>
            </svg>
          </div>
          <div className="risk-level-badge" style={{ backgroundColor: getRiskColor() }}>
            Уровень риска: {prediction?.risk_level?.toUpperCase() ?? 'Неизвестен'}
          </div>
        </div>

        <div className="ai-summary-section">
          <h3>Вывод нейронной сети</h3>
          <div className="summary-box">
            {ai_summary}
          </div>
        </div>

        <div className="models-section">
          <h3>Предсказания модели</h3>
          <div className="model-grid">
            {Object.entries(prediction?.model_predictions || {}).map(([model, value]) =>(
              <div key={model} className="model-card">
                <div className="model-name">{model.replace('_', ' ').toUpperCase()}</div>
                <div className="model-value">{(value * 100).toFixed(1)}%</div>
                <div className="model-bar">
                  <div
                    className="model-bar-fill"
                    style={{
                      width: `${value * 100}%`,
                      backgroundColor: value > 0.7 ? '#ef4444' : value > 0.3 ? '#f59e0b' : '#10b981'
                    }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="features-section">
          <h3>Факторы риска (SHAP анализ)</h3>
          <div className="features-list">
            {explanation?.top_features?.map((feature, idx) => (
              <div key={idx} className="feature-item">
                <div className="feature-name">
                  {feature?.feature_name?.replace(/_/g, ' ') || `Feature ${idx + 1}`}
                </div>
                <div className="feature-bar-container">
                  <div
                    className="feature-bar"
                    style={{
                      width: `${Math.min((feature?.importance || 0) * 100, 100)}%`,
                      backgroundColor: feature?.direction === 'positive' ? '#ef4444' : '#10b981'
                    }}
                  />
                </div>
                <div className="feature-value">
                  {(feature?.importance || 0).toFixed(3)}
                </div>
                <div className={`feature-direction ${feature?.direction || 'neutral'}`}>
                  {feature?.direction === 'positive' ? '↑ Risk' : feature?.direction === 'negative' ? '↓ Risk' : '–'}
                </div>
              </div>
            )) ?? (
              <p>Факторы недоступны</p>
            )}
          </div>
        </div>

        {court_analysis && (
          <div className="court-section">
            <h3>Анализ судебных дел</h3>
            <div className={`court-severity ${court_analysis.severity}`}>
              Серьезность: {court_analysis.severity.toUpperCase()}
            </div>
            <div className="court-analysis">
              {court_analysis.analysis}
            </div>
            {court_analysis.risk_factors.length > 0 && (
              <div className="court-factors">
                <h4>Юридические факторы риска:</h4>
                <ul>
                  {court_analysis.risk_factors.map((factor, idx) => (
                    <li key={idx}>{factor}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        <div className="company-details-section">
          <h3>Финансовые детали компании</h3>
          <div className="details-grid">
            {Object.entries(companyInfo).map(([key, value]) => (
              <div key={key} className="detail-item">
                <span className="detail-label">{key}:</span>
                <span className="detail-value">{value}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
