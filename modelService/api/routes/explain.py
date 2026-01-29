"""Эндпоинты объяснений (SHAP)"""
from fastapi import APIRouter, HTTPException, Depends
from api.schemas import PredictionRequest, ExplanationResponse, FeatureImportance
from models.ensemble import get_ensemble_model, EnsembleModel
from utils.explainers import get_shap_explainer, SHAPExplainer

router = APIRouter()


@router.post("/explain", response_model=ExplanationResponse, tags=["Explanation"])
async def explain_prediction(
    request: PredictionRequest,
    ensemble: EnsembleModel = Depends(get_ensemble_model),
    explainer: SHAPExplainer = Depends(get_shap_explainer)
):
    """Получение SHAP объяснения для прогноза банкротства"""
    try:
        shap_values = await explainer.explain(request, ensemble)

        sorted_features = sorted(
            shap_values.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )

        top_features = [
            FeatureImportance(
                feature_name=feature,
                importance=abs(value),
                direction="positive" if value > 0 else "negative"
            )
            for feature, value in sorted_features[:10]
        ]

        return ExplanationResponse(
            top_features=top_features,
            shap_values=dict(shap_values)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Explanation failed: {str(e)}"
        )
