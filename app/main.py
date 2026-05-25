from fastapi import FastAPI

from app.routes.project_routes import router as project_router
from app.routes.model_routes import router as model_router
from app.routes.evaluation_routes import router as evaluation_router
from app.routes.prediction_routes import router as prediction_router

app = FastAPI(
    title="Stock Recommendation ML API",
    description=(
        "Backend sederhana untuk dokumentasi interaktif project "
        "Machine Learning Rekomendasi Saham."
    ),
    version="1.1.0",
)

app.include_router(project_router)
app.include_router(model_router)
app.include_router(evaluation_router)
app.include_router(prediction_router)