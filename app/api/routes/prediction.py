from fastapi import APIRouter
from app.schemas.prediction_schema import PredictionRequest, PredictionResponse

router = APIRouter(
    prefix="/api/v1",
    tags=["Prediction"],
)

@router.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Predict stock recommendation",
    description="Endpoint untuk menghasilkan rekomendasi saham berdasarkan fitur teknikal.",
)
def predict_stock(request: PredictionRequest):
    """
    Endpoint prediksi sementara.
    
    Pada Tahap 1, endpoint ini hanya memastikan:
    1. API bisa menerima request JSON.
    2. Input tervalidasi oleh Pydantic.
    3. Response sudah mengikuti format PredictionResponse.
    
    Logic load model dan model.predict() akan dibuat pada tahap berikutnya.
    """

    return PredictionResponse(
        status="success",
        message="Prediction API structure is ready. Model inference will be added in the next stage.",
        prediction=None,
        confidence=None,
        probabilities=None,
        model_version="v1.0.1",
    )