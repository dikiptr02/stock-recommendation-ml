from fastapi import APIRouter, HTTPException, status

from app.schemas.prediction_schema import PredictionRequest, PredictionResponse
from app.services.model_loader import ModelLoaderError, model_loader

router = APIRouter(
    prefix="/api/v1",
    tags=["Prediction"],
)

@router.get(
        "/model-info",
        summary="Get model information",
        description="Endpoint untul mengecek informasi model yang digunakan oleh Prediction API.",
)
def get_model_info():
    """
    Endpoint untuk mamastikan model .pkl berhsil di-load.
    """
    try:
        return {
            "status": "success",
            "message": "Model loaded successfully.",
            "data": model_loader.get_model_info(),
        }
    except ModelLoaderError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
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
    
    Pada Tahap 2, service model loader sudah tersedia.
    Logic prediksi penuh akan diaktifkan pada Tahap 3.
    """

    try:
        model_loader.ensure_model_loaded()

        return PredictionResponse(
            status="success",
            message="Model loader is ready. Prediction logic will be finalized in the next stage.",
            prediction=None,
            confidence=None,
            probabilities=None,
            model_version=model_loader.version or "v1.0.1",
    )

    except ModelLoaderError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
        )