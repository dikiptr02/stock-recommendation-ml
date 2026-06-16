from fastapi import FastAPI, Request, status
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.routes.prediction_routes import router as prediction_router
from app.core.config import APP_NAME, APP_VERSION
from app.services.model_loader import model_loader
from app.routes.evaluation_routes import router as evaluation_router
from app.routes.model_routes import router as model_router
from app.routes.project_routes import router as project_router

app = FastAPI(
    title=APP_NAME,
    description="Prediction API untuk rekomendasi saham Buy, Hold, atau Sell.",
    version=APP_VERSION,
)

@app.on_event("startup")
async def startup_event():
    """
    Load model saat server boot agar request pertama tidak lambat.
    """
    model_loader.load_model()

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
):
    """
    Custom handler untuk HTTPException.

    Tujuannya agar response error dari API tidak selalu dibungkus
    di dalam key "detail" bawaan FastAPI.
    """

    detail = exc.detail

    if isinstance(detail, dict):
        return JSONResponse(
            status_code=exc.status_code,
            content=detail,
        )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": str(detail),
            "errors": [],
        },
    )


@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception,
):
    """
    Fallback handler untuk error tidak terduga.

    Tujuannya agar API tetap mengembalikan response JSON yang konsisten,
    bukan error mentah.
    """

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "message": "Unexpected internal server error.",
            "errors": [
                {
                    "field": None,
                    "message": str(exc),
                    "value": None,
                }
            ],
        },
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
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
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