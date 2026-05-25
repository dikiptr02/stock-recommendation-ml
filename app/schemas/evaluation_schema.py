from typing import Optional

from pydantic import BaseModel


class EvaluationResponse(BaseModel):
    report_version: str
    source_file: str
    accuracy: Optional[float] = None
    precision_macro: Optional[float] = None
    recall_macro: Optional[float] = None
    f1_macro: Optional[float] = None
    confusion_matrix: Optional[str] = None
    raw_report_preview: Optional[str] = None
    evaluation_status: str
    notes: Optional[str] = None