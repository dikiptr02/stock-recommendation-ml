from fastapi import FastAPI

from app.routes.project_routes import router as project_router
from app.routes.model_routes import router as model_router
from app.routes.evaluation_routes import router as evaluation_router
from app.routes.prediction_routes import router as prediction_router
from app.api.routes.prediction import router as prediction_router

app = FastAPI(
    title="Stock Recommendation Prediction API",
    description="Prediction API untuk rekomendasi saham Buy, Hold, atau Sell.",
    version="1.2.0",
)

@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Stock Recommendation Prediction API",
        "version": "1.2.0",
        "status": "running",
    }

@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "message": "prediction-api",
        "version": "1.2.0",
    }

app.include_router(project_router)
app.include_router(model_router)
app.include_router(evaluation_router)
app.include_router(prediction_router)