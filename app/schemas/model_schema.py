from typing import List, Optional

from pydantic import BaseModel

class ModelInfoResponse(BaseModel):
    model_version: str
    best_model_name: str
    model_type: str
    total_features: int
    features_used: List[str]
    target_prediction: str
    model_path: str
    model_status: str
    notes: Optional[str] = None