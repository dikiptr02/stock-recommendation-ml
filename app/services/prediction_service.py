import datetime

from app.core.config import FEATURE_COLUMNS, MODEL_VERSION_FALLBACK
from app.schemas.prediction_schema import (
    PredictionTickerRequest, 
    PredictionTickerResponse,
    BatchPredictionRequest,
    BatchPredictionResponse,
    TickerResult
)
from app.services.model_loader import model_loader


def _load_pipeline_function():
    """
    Lazy import untuk pipeline data saham.

    Tujuannya agar API tetap bisa start meskipun dependency data collection
    seperti yfinance bermasalah. Import pipeline hanya dilakukan saat endpoint
    predict by ticker atau batch benar-benar dipanggil.
    """
    try:
        from src.data_collection import download_stock_data
        from src.feature_engineering import create_features
        from src.preprocessing import preprocess_stock_data

        return download_stock_data, preprocess_stock_data, create_features

    except Exception as error:
        raise RuntimeError(
            f"Gagal memuat pipeline data saham: {error}"
        ) from error



def _normalize_ticker(ticker: str) -> str:
    """
    Memberikan format ticker agar konsisten.
    Contoh:
    - ' bbca.jk ' menjadi 'BBCA.JK'
    - 'tlkm.jk' menjadi 'TLKM.JK'
    """
    return ticker.strip().upper()

def _normalize_tickers(tickers: list[str]) -> list[str]:
    """
    Memberikan list ticker dan menghapus duplikat.
    Urutan ticker tetap dipertahankan.
    """
    cleaned_tickers = []

    for ticker in tickers:
        cleaned_ticker = _normalize_ticker(ticker)

        if cleaned_ticker and cleaned_ticker not in cleaned_tickers:
            cleaned_tickers.append(cleaned_ticker)

    return cleaned_tickers

def _get_start_date(period: str) -> str:
    """
    Mengubah period request menjadi start_date untuk download data historis.
    """
    today = datetime.date.today()
    period_str = period.lower()

    if period_str == "1y":
        return (today - datetime.timedelta(days=365)).strftime("%Y-%m-%d")

    if period_str == "5y":
        return (today - datetime.timedelta(days=5*365)).strftime("%Y-%m-%d")
    
    if period_str == "max":
        return "1900-01-01"
    
    return (today - datetime.timedelta(days=5*365)).strftime("%Y-%m-%d")

def _extract_features(latest_row, feature_data) -> dict[str, float]:
    """
    Mengambil fitur yang dibutuhkan model dari baris data terbaru.
    Semua fitur wajib tersedia agar model dapat melakukan prediksi.
    """
    missing_columns = [
        column for column in FEATURE_COLUMNS
        if column not in feature_data.columns
    ]
    if missing_columns:
        raise ValueError(
            f"Feature columns tidak lengkap. Kolom yang hilang: {missing_columns}"
        )

    return {
        column: float(latest_row[column])
        for column in FEATURE_COLUMNS
    }

def _calculate_confidence(prediction_result: dict) -> float:
    """
    Mengambil confidence dari probabilitas tertinggi.
    Jika probabilitas kosong, gunakan fallback confidence dari model_loader.
    """
    probabilities = prediction_result.get("probabilities", {})

    if probabilities:
        return max(probabilities.values())

    return prediction_result.get("confidence", 0.0)

def _format_latest_data_date(latest_row) -> str:
    """
    Mengubah tanggal data terbaru menjadi string.
    """
    if hasattr(latest_row["Date"], "date"):
        return str(latest_row["Date"].date())
    
    return str(latest_row["Date"])
    

def predict_by_ticker(request: PredictionTickerRequest) -> PredictionTickerResponse:
    """
    Fungsi untuk memprediksi rekomendasi saham berdasarkan ticker.
    Mengambil data secara in-memory, tanpa menyimpan file CSV fisik.
    """
    ticker = _normalize_ticker(request.ticker)
    start_date = _get_start_date(request.period)

    download_stock_data, preprocess_stock_data, create_features = _load_pipeline_functions()

    raw_data = download_stock_data(
        ticker=ticker,
        start_date=start_date,
        save_file=False
    )

    clean_data = preprocess_stock_data(
        input_data=raw_data,
        save_file=False
    )
    
    feature_data = create_features(
        input_data=clean_data,
        save_file=False
    )

    if feature_data.empty:
        raise ValueError(
            f"Data fitur untuk ticker {ticker} kosong. "
            "Kemungkinan data historis terlalu sedikit atau ticker tidak valid."
        )
    
    latest_row = feature_data.iloc[-1]
    features_used = _extract_features(latest_row, feature_data)

    prediction_result = model_loader.predict(features_used)
    
    probabilities = prediction_result.get("probabilities", {})
    confidence = _calculate_confidence(prediction_result)
    latest_data_date = _format_latest_data_date(latest_row)
    
    return PredictionTickerResponse(
        status="success",
        ticker=ticker,
        period=str(request.period),
        model_version=model_loader.version or MODEL_VERSION_FALLBACK,
        model_name=model_loader.model_name or "stock_model",
        latest_data_date=latest_data_date,
        latest_close_price=float(latest_row["Close"]),
        features_used=features_used,
        recommendation=prediction_result["prediction"],
        confidence=confidence,
        probabilities=probabilities,
    )


def predict_batch(request: BatchPredictionRequest) -> BatchPredictionResponse:
    """
    Fungsi untuk memprediksi rekomendasi saham untuk banyak ticker sekaligus (batch).
    Sistem memproses setiap ticker secara berurutan (sequential).
    """
    normalized_tickers = _normalize_tickers(request.tickers)

    if not normalized_tickers:
        raise ValueError("Daftar ticker kosong setelah dinormalisasi.")

    # Daftar untuk menyimpan hasil tiap ticker, baik yang sukses maupun gagal
    results = []
    
    total_success = 0
    total_failed = 0
    
    # Melakukan perulangan untuk setiap ticker yang di-request user
    for ticker in normalized_tickers:
        try:
            # Mempersiapkan request tunggal untuk ticker yang sedang diproses
            single_request = PredictionTickerRequest(
                ticker=ticker, 
                period=request.period,
            )
            
            # Memanggil logic prediksi tunggal yang sudah dibuat di versi 1.3.0
            single_response = predict_by_ticker(single_request)
            
            # Jika berhasil, simpan hasilnya dengan status success
            results.append(
                TickerResult(
                    ticker=ticker,
                    status="success",
                    latest_data_date=single_response.latest_data_date,
                    latest_close_price=single_response.latest_close_price,
                    recommendation=single_response.recommendation,
                    confidence=single_response.confidence,
                    probabilities=single_response.probabilities,
                )
            )
            
            # Menambah counter sukses
            total_success += 1
            
        except Exception as error:
            # Jika gagal (misal salah ketik ticker atau tidak ada koneksi), tangkap errornya
            results.append(
                TickerResult(
                    ticker=ticker,
                    status="error",
                    message=str(error),
                )
            )
            
            # Menambah counter gagal
            total_failed += 1
            
    # Menentukan status akhir API (success jika minimal ada 1 yang berhasil, error jika semua gagal)
    overall_status = "success" if total_success > 0 else "error"
    
    # Menyusun respons akhir yang menggabungkan seluruh ringkasan dan detail hasil ticker
    return BatchPredictionResponse(
        status=overall_status,
        total_requested=len(normalized_tickers),
        total_success=total_success,
        total_failed=total_failed,
        results=results
    )