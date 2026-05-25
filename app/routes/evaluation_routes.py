from fastapi import APIRouter

from app.schemas.evaluation_schema import EvaluationResponse
from app.services.evaluation_service import get_evaluation_summary

router = APIRouter(
    tags=["Evaluation"]
)

@router.get("/evaluation", response_model=EvaluationResponse)
def evaluation():
    return get_evaluation_summary()