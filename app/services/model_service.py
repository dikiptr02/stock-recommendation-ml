from pathlib import Path
from typing import Any

import joblib

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = PROJECT_ROOT / "models" / "stock_model_v1.0.1.pkl"

def _load_model_artifact() -> dict[str, Any] | None:
    """
    Membaca file model .pkl dari versi v1.0.1.
    
    File model disimpan dalam bentuk dictionary dengan key:
    - version
    - model_name
    - model
    - feature_columns
    - target_column
    - results
    """

    try:
        if not MODEL_PATH.exists():
            return None
        
        artifact = joblib.load(MODEL_PATH)

        if not isinstance(artifact, dict):
            return None
        
        return artifact
    
    except Exception:
        return None
    
def get_model_info() -> dict:
    """
    Mengambil informasi model untuk ditampilkan melalui endpoint /model-info.
    Backend v1.1.0 hanya membaca artefak model, tidak melakukan training ulang.
    """
    artifact = _load_model_artifact()

    if artifact is None:
        return {
            "model_version": "unknown",
            "best_model_name": "unknown",
            "model_type": "unknown",
            "total_features": 0,
            "features_used": [],
            "target_prediction": "unknown",
            "model_path": str(MODEL_PATH),
            "model_status": "Model file not found or failed to load",
            "notes": (
                "Pastikan file models/stock_model_v1.0.1.pkl tersedia "
                "dan dapat dibaca oleh joblib"
            ),
        }

    model_object = artifact.get("model")
    feature_columns = artifact.get("feature_columns", [])

    if feature_columns is None:
        feature_columns = []

    model_type = type(model_object).__name__ if model_object is not None else "unknown"

    return {
        "model_version": artifact.get("version", "v1.0.1"),
        "best_model_name": artifact.get("model_name", model_type),
        "model_type": model_type,
        "total_features": len(feature_columns),
        "features_used": feature_columns,
        "target_prediction": artifact.get("target_column", "Buy, Hold, or Sell"),
        "model_path": str(MODEL_PATH),
        "model_status": "Model loaded successfully",
        "notes": (
            "Model ini adalah artefak dari versi v1.0.1. "
            "Backend v1.1.0 hanya membaca informasi model dan belum "
            "melakukan training ulang atau prediksi real-time."
        ),
    }