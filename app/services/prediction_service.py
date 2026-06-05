import pandas as pd
import datetime

from app.schemas.prediction_schema import PredictionTickerRequest, PredictionTickerResponse
from src.data_collection import download_stock_data
from src.preprocessing import preprocess_stock_data
from src.feature_engineering import create_features
from app.services.model_loader import model_loader


def predict_by_ticker(request: PredictionTickerRequest) -> PredictionTickerResponse:
    """
    Fungsi untuk memprediksi rekomendasi saham berdasarkan ticker.
    Mengambil data secara in-memory, tanpa menyimpan file CSV fisik.
    """
    # Menentukan rentang tanggal awal berdasarkan period yang direquest user
    today = datetime.date.today()
    period_str = request.period.lower()
    
    if period_str == "1y":
        start_date = (today - datetime.timedelta(days=365)).strftime("%Y-%m-%d")
    elif period_str == "5y":
        start_date = (today - datetime.timedelta(days=5*365)).strftime("%Y-%m-%d")
    elif period_str == "max":
        start_date = "1900-01-01"
    else:
        start_date = (today - datetime.timedelta(days=5*365)).strftime("%Y-%m-%d")
        
    # Mengambil data historis saham berdasarkan ticker dari request user tanpa membuat file CSV
    raw_data = download_stock_data(
        ticker=request.ticker,
        start_date=start_date,
        save_file=False
    )
    
    # Membersihkan data mentah langsung di memory (in-memory preprocessing)
    clean_data = preprocess_stock_data(
        input_data=raw_data,
        save_file=False
    )
    
    # Membuat indikator teknikal dari data bersih langsung di memory
    feature_data = create_features(
        input_data=clean_data,
        save_file=False
    )
    
    # Mengambil baris terakhir karena prediksi menggunakan kondisi data paling terbaru
    latest_row = feature_data.iloc[-1]
    
    # Memilih nilai fitur teknikal yang sesuai dengan kebutuhan input model v1.0.1
    features_used = {
        col: float(latest_row[col]) for col in ["Daily_Return", "MA_5", "MA_10", "RSI", "Volatility", "Volume_Change"]
        if col in feature_data.columns
    }
    
    # Memasukkan fitur teknikal ke model machine learning untuk diprediksi
    prediction_result = model_loader.predict(features_used)
    
    # Confidence diambil dari probabilitas tertinggi hasil prediksi model
    probabilities = prediction_result.get("probabilities", {})
    if probabilities:
        confidence = max(probabilities.values())
    else:
        confidence = prediction_result.get("confidence", 0.0)
        
    if hasattr(latest_row["Date"], "date"):
        latest_data_date = str(latest_row["Date"].date())
    else:
        latest_data_date = str(latest_row["Date"])

    # Menyusun format data akhir untuk dikembalikan sebagai response API
    response = PredictionTickerResponse(
        status="success",
        ticker=request.ticker,
        period=request.period,
        model_version=model_loader.version or "v1.0.1",
        model_name=model_loader.model_name or "stock_model",
        latest_data_date=latest_data_date,
        latest_close_price=float(latest_row["Close"]),
        features_used=features_used,
        recommendation=prediction_result["prediction"],
        confidence=confidence,
        probabilities=probabilities,
    )
    
    return response