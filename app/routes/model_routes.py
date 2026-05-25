from fastapi import APIRouter

from app.schemas.model_schema import ModelInfoResponse
from app.services.model_service import get_model_info

router = APIRouter(
    tags=["Model"]
)

@router.get("/model-info", response_model=ModelInfoResponse)
def model_info():
    return get_model_info()