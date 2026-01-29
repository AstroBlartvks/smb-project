from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from api.schemas import (
    CourtCaseRequest, CourtCaseAnalysis,
    ComprehensiveAnalysisRequest, ComprehensiveAnalysisResponse,
    PredictionRequest, PredictionResponse, ExplanationResponse,
    ModelPrediction, FeatureImportance
)
from models.ensemble import get_ensemble_model, EnsembleModel
from models.qwen_model import qwen_model
from utils.explainers import get_shap_explainer, SHAPExplainer
from preprocessing.feature_engineering import create_features
from config import settings

router = APIRouter()


def get_risk_level(probability: float) -> str:
    """Определение уровня риска на основе вероятности"""
    if probability < settings.LOW_RISK_THRESHOLD:
        return "low"
    elif probability < settings.HIGH_RISK_THRESHOLD:
        return "medium"
    else:
        return "high"


@router.post("/analyze-court", response_model=CourtCaseAnalysis, tags=["Analysis"])
async def analyze_court_cases(request: CourtCaseRequest):
    """Анализ судебных дел компании"""
    try:
        analysis = qwen_model.analyze_court_cases(request.court_data)
        return CourtCaseAnalysis(**analysis)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Court analysis failed: {str(e)}")


@router.post("/comprehensive", response_model=ComprehensiveAnalysisResponse, tags=["Analysis"])
async def comprehensive_analysis(
    request: ComprehensiveAnalysisRequest,
    ensemble: EnsembleModel = Depends(get_ensemble_model),
    explainer: SHAPExplainer = Depends(get_shap_explainer)
):
    """Комплексный анализ компании с прогнозом банкротства"""
    try:
        pred_request = PredictionRequest(**request.model_dump())

        predictions = await ensemble.predict(pred_request)
        bankruptcy_prob = predictions['ensemble'] * 100

        prediction_response = PredictionResponse(
            bankruptcy_probability=round(bankruptcy_prob, 2),
            risk_level=get_risk_level(predictions['ensemble']),
            model_predictions=ModelPrediction(**predictions),
            timestamp=datetime.now()
        )

        shap_values = await explainer.explain(pred_request, ensemble)
        sorted_features = sorted(shap_values.items(), key=lambda x: abs(x[1]), reverse=True)

        top_features = [
            FeatureImportance(
                feature_name=feature,
                importance=abs(value),
                direction="positive" if value > 0 else "negative"
            )
            for feature, value in sorted_features[:10]
        ]

        explanation_response = ExplanationResponse(
            top_features=top_features,
            shap_values=dict(shap_values)
        )

        court_analysis_result = None
        if request.court_data:
            court_result = qwen_model.analyze_court_cases(request.court_data)
            court_analysis_result = CourtCaseAnalysis(**court_result)

        company_data_dict = request.model_dump()
        features = create_features(pred_request)
        company_data_dict.update(features)

        ai_summary = qwen_model.generate_summary(
            company_data_dict,
            prediction_response.model_dump(),
            court_analysis_result.model_dump() if court_analysis_result else {}
        )

        return ComprehensiveAnalysisResponse(
            prediction=prediction_response,
            explanation=explanation_response,
            court_analysis=court_analysis_result,
            ai_summary=ai_summary,
            timestamp=datetime.now()
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comprehensive analysis failed: {str(e)}")
