from fastapi import APIRouter

from app.schemas.prediction_schema import PredictionResponse
from app.services.prediction_service import get_latest_prediction

router = APIRouter(
    tags=["Prediction"]
)

@router.get("/prediction", response_model=PredictionResponse)
def prediction():
    return get_latest_prediction()