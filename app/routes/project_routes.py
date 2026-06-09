from fastapi import APIRouter
from app.core.config import APP_VERSION

router = APIRouter(
    tags=["Project"]
)

@router.get("/project-info")
def project_info():
    return {
        "project_name": "Machine Learning Rekomendasi Saham",
        "version": APP_VERSION,
        "goal": (
            "Membangun backend sederhana menggunakan FastAPI untuk  "
            "menampilkan informasi project, model, evaluasi, dan prediksi."
        ),
        "description": (
            "Project ini memiliki pipeline machine learning untuk menghasilkan "
            "rekomendasi saham Buy, Hold, atau Sell. Pada versi API saat ini, "
            "project sudah mendukung prediksi manual, prediksi berdasarkan ticker, "
            "dan batch prediction untuk beberapa ticker."
        ),
        "main_features": [
            "Menampilkan informasi project",
            "Menampilkan informasi model baseline",
            "Menampilkan ringkasan evaluasi model",
            "Prediksi otomatis berdasarkan ticker saham",
            "Prediksi otomatis berdasarkan ticker saham",
            "Batch prediction untuk beberapa ticker",
            "Dokumentasi interaktif melalui Swagger UI",
        ],
        "ml_pipeline": [
            "Data_Collection",
            "Preprocessing",
            "Feature_Engineering",
            "Labeling",
            "Training_Model",
            "Evaluation_Model",
            "Prediction",
        ],
        "api_features": [
            "FastAPI backend",
            "Manual prediction endpoint",
            "Prediction by ticker endpoint",
            "Batch prediction endpoint",
            "Centralized API configuration",
            "Request validation with Pydantic",
        ],
        "disclaimer": (
            "Project ini hanya untuk pembelajaran dan portofolio. "
            "Hasil prediksi bukan nasihat investasi."
        ),
    }

@router.get("/docs-summary")
def docs_summary():
    return {
        "title": "Dokumentasi Project Machine Learning Rekomendasi Saham",
        "version": APP_VERSION,
        "summary": (
            "Project ini membangun pipeline machine learning dan backend API "
            "untuk memberikan rekomendasi saham berupa Buy, Hold, atau Sell. "
            "Versi saat ini berfokus pada API prediction, validasi input, "
            "batch prediction, dan kerapian struktur project."
        ),
        "model_artifact": "models/stock_model_v1.0.1.pkl",
        "report_files": [
            "reports/evaluation_v1.0.1.md",
            "reports/prediction_v1.0.1.md",
        ],
        "available_endpoints": [
            "GET /",
            "GET /health",
            "GET /project-info",
            "GET /docs-summary",
            "GET /model-info",
            "GET /evaluation",
            "GET /api/v1/model-info",
            "POST /api/v1/predict",
            "POST /api/v1/predict/ticker",
            "POST /api/v1/predict/batch",
        ],
        "notes": (
            "API saat ini menggunakan model baseline dari v1.0.1. "
            "Belum ada training ulang otomatis, database history prediction, "
            "atau frontend dashboard."
        ),
        "future_development": [
            "Menambahkan automated testing untuk endpoint API",
            "Menambahkan logging",
            "Meningkatkan performa model machine learning",
            "Menambahkan backtesting",
            "Menyimpan hasil prediksi ke database",
            "Membangun dashboard frontend",
        ],
    }