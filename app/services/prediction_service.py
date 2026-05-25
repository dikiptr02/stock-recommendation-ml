from pathlib import Path
import re
from typing import Any

import pandas as pd

PROJECT_ROOT =Path(__file__).resolve().parents[2]

PREDICTION_REPORT_PATH = PROJECT_ROOT / "reports" / "prediction_v1.0.1.md"
LABELED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "BBCA_JK_labeled.csv"

def _read_prediction_report() -> str:
    """
    Membaca isi file reports/prediction_v1.0.1.md.
    """
    if not PREDICTION_REPORT_PATH.exists():
        return ""
    
    return PREDICTION_REPORT_PATH.read_text(encoding="utf-8")

def _safe_float(value: Any) -> float | None:
    """
    Mengubah nilai menjadi float dengan aman.
    Jika gagal atau nilainya kosong, return None.
    """
    try:
        if pd.isna(value):
            return None
        return float(value)
    except (ValueError, TypeError):
        return None
    
def _extract_table_value(text: str, aliases: list[str]) -> str | None:
    """
    Mengambil value dari tabel Markdown
    
    Contoh:
    | Tanggal data terbaru | 2026-05-19 |
    | Harga Close terbaru | 5950.00 |
    | Rekomendasi model | Hold |
    """
    for alias in aliases:
        pattern = rf"\|\s*{alias}\s*\|\s*([^|\n]+?)\s*\|"
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).strip()

    return None
    
def _extract_recommendation(text: str) -> str | None:
    """
    Mengambil rekomendasi Buy/Hold/Sell dari laporan prediksi.
    
    Bisa membaca format:
    - Recommendation: Hold
    - Rekomendasi = Buy
    - Prediction: Sell
    - | Recommendation | Hold |
    """
    patterns = [
        r"(?:recommendation|rekomendasi|prediction|prediksi)\s*[:=]\s*(Buy|Hold|Sell)",
        r"\|\s*[^|\n]*(?:recommendation|rekomendasi|prediction|prediksi)[^|\n]*\|\s*(Buy|Hold|Sell)\s*\|",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).capitalize()

    return None

def _extract_probability(text: str, label:str) -> float | None:
    """
    Mengambil probabilitas untuk label Buy, Hold, atau Sell.
    
    Bisa membaca format:
    - Buy: 0.25
    - Probability Buy: 0.25
    - | Buy | 0.25 |
    """
    patterns = [
        rf"{label}\s*[:=]\s*([0-9]*\.?[0-9]+)",
        rf"probability\s+{label}\s*[:=]\s*([0-9]*\.?[0-9]+)",
        rf"probabilitas\s+{label}\s*[:=]\s*([0-9]*\.?[0-9]+)",
        rf"\|\s*{label}\s*\|\s*([0-9]*\.?[0-9]+)\s*\|",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return _safe_float(match.group(1))
        
    return None

def _get_latest_data_info() -> tuple[str | None, float | None, str | None]:
    """
    Mengambil tanggal terbaru, harga close terbaru, dan rekomendasi terbaru
    dari data labeled.
    """
    if not LABELED_DATA_PATH.exists():
        return None, None, None
    
    df = pd.read_csv(LABELED_DATA_PATH)

    if df.empty:
        return None, None, None
    
    latest_row = df.iloc[-1]

    date_candidates = [
        "Date",
        "date",
        "Tanggal",
        "tanggal",
        "Datetime",
        "datetime",
    ]

    close_candidates = [
        "Close",
        "close",
        "Adj Close",
        "adj_close",
        "Close_Price",
        "close_price",
    ]

    recommendation_candidates = [
        "Recommendation",
        "recommendation",
        "Prediction",
        "prediction",
        "Prediksi",
        "prediksi",
        "Label",
        "label",
        "Target",
        "target",
    ]

    latest_date = None
    latest_close = None
    latest_recommendation = None

    for col in date_candidates:
        if col in df.columns:
            latest_date = str(latest_row[col])
            break

    for col in close_candidates:
        if col in df.columns:
            latest_close = _safe_float(latest_row[col])
            break

    for col in recommendation_candidates:
        if col in df.columns:
            value = latest_row[col]
            if not pd.isna(value):
                latest_recommendation = str(value)
            break

    return latest_date, latest_close, latest_recommendation

def get_latest_prediction() -> dict:
    """
    Mengambil hasil prediksi terbaru untuk ditampilkan melalui endpoint /prediction.
    Backend v1.0.1 hanya membaca hasil prediksi dari v1.0.1.
    """
    report_text = _read_prediction_report()

    report_latest_date = _extract_table_value(
        report_text,
        aliases=[
            "Tanggal data terbaru",
            "Latest data date",
            "Latest date",
        ],
    )

    report_latest_close = _extract_table_value(
        report_text,
        aliases=[
            "Harga Close terbaru",
            "Latest close price",
            "Close terbaru",
        ],
    )

    latest_date, latest_close, recommendation_from_data = _get_latest_data_info()
    recommendation_from_report = _extract_recommendation(report_text)

    recommendation = recommendation_from_report or recommendation_from_data

    probabilities = {
        "Buy": _extract_probability(report_text, "Buy"),
        "Hold": _extract_probability(report_text, "Hold"),
        "Sell": _extract_probability(report_text, "Sell"),
    }

    probabilities = {
        key: value
        for key, value in probabilities.items()
        if value is not None
    }

    if not report_text:
        prediction_status = "Prediction report file not found"
        notes = (
            "Pastikan file reports/prediction_v1.0.1.md tersedia. "
            "Backend masih mencoba membaca informasi terbaru dari data labeled."
        )
    else:
        prediction_status = "Prediction report loaded successfully"
        notes = (
            "Hasil prediksi dibaca dari reports/prediction_v1.0.1.md "
            "dan data/processed/BBCA_JK_labeled.csv. "
            "Backend v1.1.0 belum melakukan prediksi real-time."
        )

    return {
        "source_file": str(PREDICTION_REPORT_PATH),
        "data_file": str(LABELED_DATA_PATH),
        "model_version": "v1.0.1",
        "latest_data_date": report_latest_date or latest_date,
        "latest_close_price": _safe_float(report_latest_close) or latest_close,
        "recommendation": recommendation,
        "probabilities": probabilities if probabilities else None,
        "raw_report_preview": report_text[:1000] if report_text else None,
        "prediction_status": prediction_status,
        "notes": notes,
    }