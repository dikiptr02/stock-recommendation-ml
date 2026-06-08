from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.config import APP_NAME, APP_VERSION
from app.routes.project_routes import router as project_router
from app.routes.model_routes import router as model_router
from app.routes.evaluation_routes import router as evaluation_router
from app.api.routes.prediction import router as prediction_router

app = FastAPI(
    title=APP_NAME,
    description="Prediction API untuk rekomendasi saham Buy, Hold, atau Sell.",
    version=APP_VERSION,
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, 
    exc: RequestValidationError,
):
    """
    Custom handler untuk error validasi request.

    Tujuannya agar error input dari user lebih mudah dibaca.
    """

    formatted_errors = []

    for error in exc.errors():
        location = error.get("loc", [])
        field = location[-1] if location else None

        formatted_errors.append(
            {
                "field": field,
                "message": error.get("msg"),
                "value": error.get("input"),
            }
        )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": "error",
            "message": "Invalid request input.",
            "errors": formatted_errors,
        },
    )

@app.get("/", tags=["Root"])
def root():
    return {
        "message": APP_NAME,
        "version": APP_VERSION,
        "status": "running",
    }

@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "message": "prediction-api",
        "version": APP_VERSION,
    }

app.include_router(project_router)
app.include_router(model_router)
app.include_router(evaluation_router)
app.include_router(prediction_router)