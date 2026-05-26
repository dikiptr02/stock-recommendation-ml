from typing import Dict, Optional
from pydantic import BaseModel, Field

class PredictionRequest(BaseModel):
    """
    Schema input endpoint prediksi saham.

    Semua field ini harus sama dengan feature_columns
    yang ditemukan pada model v1.0.1.
    """

    Daily_Return: float = Field(
        ...,
        description="Return harian saham..",
        example=0.012,
    )
    MA_5: float = Field(
        ...,
        description="Moving average 5 hari.",
        example=102.5,
    )
    MA_10: float = Field(
        ...,
        description="Moving average 10 hari.",
        example=101.8,
    )
    RSI: float = Field(
        ...,
        description="Relative Strength Index.",
        example=55.2,
    )
    Volatility: float = Field(
        ...,
        description="Volatilitas harga saham.",
        example=0.03,
    )
    Volume_Change: float = Field(
        ...,
        description="Perubahan volume transaksi.",
        example=0.12,
    )

class PredictionResponse(BaseModel):
    """
    Schema output dari endpoint prediksi saham.
    """

    status: str = Field(
        ...,
        description="Status response API.",
        example="success",
    )
    message: str = Field(
        ...,
        description="Pesan singkat dari API.",
        example="Prediction endpoint is ready.",
    )
    prediction: Optional[str] = Field(
        default=None,
        description="Hasil rekomendasi model: Buy, Hold, atau Sell.",
        example="Buy",
    )
    confidence: Optional[float] = Field(
        default=None,
        description="Probabilitas tertinggi dari hasil prediksi.",
        example=0.87,
    )
    probabilities: Optional[Dict[str, float]] = Field(
        default=None,
        description="Probabilitas untuk setiap class.",
        example={
            "Buy": 0.87,
            "Hold": 0.10,
            "Sell": 0.03,
        },
    )
    model_version: str = Field(
        default="v1.0.1",
        description="Versi model yang digunakan.",
        example="v1.0.1",
    )