from typing import Dict, Optional, Any, List
from pydantic import BaseModel, Field

class PredictionRequest(BaseModel):
    """
    Schema input untuk endpoint prediksi saham.

    Semua field ini harus sama dengan feature_columns
    yang ditemukan pada model v1.0.1:
    - Daily_Return
    - MA_5
    - MA_10
    - RSI
    - Volatility
    - Volume_Change
    """

    Daily_Return: float = Field(
        ...,
        ge=-1.0,
        le=1.0,
        description="Return harian saham. Range wajar: -1.0 sampai 1.0.",
        example=0.012,
    )
    MA_5: float = Field(
        ...,
        gt=0,
        description="Moving average 5 hari. Harus lebih besar dari 0.",
        example=102.5,
    )
    MA_10: float = Field(
        ...,
        gt=0,
        description="Moving average 10 hari. Harus lebih besar dari 0.",
        example=101.8,
    )
    RSI: float = Field(
        ...,
        ge=0,
        le=100,
        description="Relative Strength Index. Range valid: 0 sampai 100.",
        example=55.2,
    )
    Volatility: float = Field(
        ...,
        ge=0,
        le=1.0,
        description="Volatilitas harga saham. Range wajar: 0 sampai 1.0.",
        example=0.03,
    )
    Volume_Change: float = Field(
        ...,
        ge=-1.0,
        le=10.0,
        description="Perubahan volume transaksi. Range wajar: -1.0 sampai 10.0.",
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
        example="Prediction completed successfully.",
    )
    prediction: Optional[str] = Field(
        default=None,
        description="Hasil rekomendasi model: Buy, Hold, atau Sell.",
        example="Buy",
    )
    confidence: Optional[float] = Field(
        default=None,
        description="Probabilitas tertinggi dari hasil prediksi.",
        example=0.625,
    )
    probabilities: Optional[Dict[str, float]] = Field(
        default=None,
        description="Probabilitas untuk setiap class.",
        example={
            "Buy": 0.625,
            "Hold": 0.325,
            "Sell": 0.05,
        },
    )
    model_version: str = Field(
        default="v1.0.1",
        description="Versi model yang digunakan.",
        example="v1.0.1",
    )

class PredictionTickerRequest(BaseModel):
    ticker: str = Field(..., description="Kode ticker saham (contoh: BBCA.JK)")
    period: str = Field("5y", description="Periode data historis (contoh: 1y, 5y, max)")

class PredictionTickerResponse(BaseModel):
    status: str = Field(..., description="Status response API", example="success")
    ticker: str = Field(..., description="Kode ticker saham")
    period: str = Field(..., description="Periode yang digunakan")
    model_version: str = Field(..., description="Versi model")
    model_name: str = Field(..., description="Nama model")
    latest_data_date: str = Field(..., description="Tanggal data terbaru")
    latest_close_price: float = Field(..., description="Harga close terbaru")
    features_used: Dict[str, Any] = Field(..., description="Fitur teknikal yang digunakan")
    recommendation: str = Field(..., description="Rekomendasi Buy, Hold, atau Sell")
    confidence: float = Field(..., description="Nilai confidence prediksi")
    probabilities: Dict[str, float] = Field(..., description="Probabilitas masing-masing label")

# --- SCHEMA UNTUK BATCH PREDICTION (v1.4.0) ---

class BatchPredictionRequest(BaseModel):
    """
    Schema input (Request) untuk memprediksi banyak saham sekaligus.
    User akan mengirim list berisi beberapa ticker dan periode datanya.
    """
    tickers: List[str] = Field(..., description="Daftar kode ticker saham (contoh: ['BBCA.JK', 'TLKM.JK'])")
    period: str = Field("5y", description="Periode data historis (contoh: 1y, 5y, max)")

class TickerResult(BaseModel):
    """
    Schema untuk menyimpan detail hasil dari masing-masing individu ticker.
    Jika sukses, berisi harga, rekomendasi, dll.
    Jika gagal, field rekomendasi dll akan kosong, namun field 'message' akan berisi alasan gagalnya.
    """
    ticker: str = Field(..., description="Kode ticker saham")
    status: str = Field(..., description="Status prediksi untuk ticker ini: 'success' atau 'error'")
    message: Optional[str] = Field(default=None, description="Pesan detail jika status error")
    latest_data_date: Optional[str] = Field(default=None, description="Tanggal data terbaru")
    latest_close_price: Optional[float] = Field(default=None, description="Harga close terbaru")
    recommendation: Optional[str] = Field(default=None, description="Rekomendasi Buy, Hold, atau Sell")
    confidence: Optional[float] = Field(default=None, description="Nilai confidence prediksi")
    probabilities: Optional[Dict[str, float]] = Field(default=None, description="Probabilitas masing-masing label")

class BatchPredictionResponse(BaseModel):
    """
    Schema output (Response) untuk endpoint batch prediction.
    Berisi rekapitulasi jumlah request yang sukses/gagal beserta detail (results) dari setiap ticker.
    """
    status: str = Field(..., description="Status respons keseluruhan API", example="success")
    total_requested: int = Field(..., description="Jumlah ticker yang di-request")
    total_success: int = Field(..., description="Jumlah ticker yang berhasil diproses")
    total_failed: int = Field(..., description="Jumlah ticker yang gagal diproses")
    results: List[TickerResult] = Field(..., description="Daftar detail hasil untuk setiap ticker")