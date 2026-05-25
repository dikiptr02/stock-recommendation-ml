from typing import Dict, Optional

from pydantic import BaseModel

class PredictionResponse(BaseModel):
    source_file: str
    data_file: str
    model_version: str
    latest_data_date: Optional[str] = None
    latest_close_price: Optional[float] = None
    recommendation: Optional[str] = None
    probabilities: Optional[Dict[str, float]] = None
    raw_report_preview: Optional[str] = None
    prediction_status: str
    notes: Optional[str] = None