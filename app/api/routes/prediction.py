from fastapi import APIRouter, HTTPException, status

from app.schemas.prediction_schema import (
    PredictionRequest, 
    PredictionResponse, 
    PredictionTickerRequest, 
    PredictionTickerResponse,
    BatchPredictionRequest,
    BatchPredictionResponse
)
from app.services.model_loader import ModelLoaderError, model_loader
from app.services.prediction_service import predict_by_ticker, predict_batch

router = APIRouter(
    prefix="/api/v1",
    tags=["Prediction"],
)

@router.get(
        "/model-info",
        summary="Get model information",
        description="Endpoint untuk mengecek informasi model yang digunakan oleh Prediction API.",
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
            detail={
                "status": "error",
                "message": "Failed to load model information.",
                "error": [
                    {
                        "field": None,
                        "message": str(error),
                        "value": None,
                    }
                ],
            },
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

    Alur:
    1. Menerima input JSON dari user.
    2. Validasi otomatis oleh Pydantic.
    3. Mengubah request menjadi dictionary.
    4. Mengirim input ke model_loader.predict().
    5. Mengembalikan hasil prediksi, confidence, dan probabilitas.
    """

    try:
        input_data = (
            request.model_dump()
            if hasattr(request, "model_dump")
            else request.dict()
        )

        prediction_result = model_loader.predict(input_data)

        return PredictionResponse(
            status="success",
            message="Prediction completed successfully.",
            prediction=prediction_result["prediction"],
            confidence=prediction_result["confidence"],
            probabilities=prediction_result["probabilities"],
            model_version=model_loader.version or "v1.0.1",
    )

    except ModelLoaderError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "error",
                "message": "model prediction failed.",
                "errors": [
                    {
                        "field": None,
                        "message": str(error),
                        "value": None,
                    }
                ],
            },
        )
    
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "error",
                "message": "Prediction failed.",
                "errors": [
                    {
                        "field": None,
                        "message": str(error),
                        "value": None,
                    }
                ],
            },
        )

@router.post(
    "/predict/ticker",
    response_model=PredictionTickerResponse,
    summary="Predict stock recommendation by ticker",
    description="Endpoint untuk menghasilkan rekomendasi saham dengan menginput ticker (contoh: BBCA.JK). Data akan diproses in-memory.",
)
def predict_stock_by_ticker(request: PredictionTickerRequest):
    try:
        return predict_by_ticker(request)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "error",
                "message": "Prediction by ticker failed.",
                "errors": [
                    {
                        "field": None,
                        "message": str(error),
                        "value": None,
                    }
                ],
            },
        )

@router.post(
    "/predict/batch",
    response_model=BatchPredictionResponse,
    summary="Predict stock recommendation for multiple tickers (batch)",
    description="Endpoint untuk menghasilkan rekomendasi saham dengan menginput beberapa ticker sekaligus (contoh: ['BBCA.JK', 'TLKM.JK']). Data akan diproses secara berurutan.",
)
def predict_stock_batch(request: BatchPredictionRequest):
    """
    Menerima request batch prediction.
    Akan memanggil service predict_batch yang akan memproses tiap ticker secara aman.
    Jika satu ticker gagal, ticker lainnya akan tetap diproses.
    """
    try:
        return predict_batch(request)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "error",
                "message": "Batch prediction failed due to internal error.",
                "errors": [
                    {
                        "field": None,
                        "message": str(error),
                        "value": None,
                    }
                ],
            },
        )