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
            "Hasil Versi v1.1.0 berfokus pada perombakan sistem dokumentasi "
            "dengan menambahkan backend API sederhana. Backend ini membaca "
            "hasil pipeline dari v1.0.1 tanpa melakukan training ulang."
        ),
        "main_features": [
            "Menampilkan informasi project",
            "Menampilkan informasi model terbaik",
            "Menampilkan ringkasan evaluasi model",
            "Menampilkan hasil prediksi terbaru",
            "Menyediakan dokumentasi interaktif melalui Swagger UI",
        ],
        "ml_pipeline_v1_0_1": [
            "Data_Collection",
            "Preprocessing",
            "Feature_Engineering",
            "Labeling",
            "Training_Model",
            "Evaluation_Model",
            "Prediction",
        ],
        "backend_focus_v1_1_0": [
            "Membuat backend sederhana menggunakan FastAPI",
            "Membaca artefak hasil pipeline v1.0.1",
            "Menampilkan informasi model melalui API",
            "Menampilkan evaluasi model melalui API",
            "Menampilkan hasil prediksi melalui API",
            "Menyiapkan pondasi menuju API prediksi atau dashboard",
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
            "Project ini membangun pipeline machine learning untuk memberikan "
            "rekomendasi saham berupa Buy, Hold, atau Sell. Pada versi v1.1.0, "
            "project dikembangkan dengan backend FastAPI agar hasil model, "
            "evaluasi, dan prediksi dapat diakses secara interaktif."
        ),
        "available_files_from_v1.0.1": [
            "models/stock_model_v1.0.1.pkl",
            "reports/evaluation_v1.0.1.md",
            "reports/prediction_v1.0.1.md",
            "data/processed/BBCA_JK_labeled.csv",
            "data/processed/BBCA_JK_features.csv",
        ],
        "available_endpoints": [
            "GET /",
            "GET /project-info",
            "GET /model-info",
            "GET /evaluation",
            "GET /prediction",
            "GET /docs-summary",
        ],
        "notes": (
            "Backend v1.1.0 berfungsi sebagai dokumentasi interaktif. "
            "Backend belum melakukan training ulang dan belum menyediakan "
            "prediksi real-time dari input user."
        ),
        "future_development": [
            "Menambahkan endpoint prediksi real-time",
            "Menambahkan dukungan multi saham",
            "Menambahkan database",
            "Membuat dashboard frontend",
            "Deploy backend ke cloud",
        ],
    }