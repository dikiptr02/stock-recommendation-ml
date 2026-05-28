from pathlib import Path
from typing import Any, Dict, List, Optional

import joblib
import pandas as pd

class ModelLoaderError(Exception):
    """
    Custom error untuk masalah load model.
    """
    pass

class StockModelLoader:
    """
    Service untuk load model saham dari file .pkl.
    
    File model v1.0.1 berbentuk dictionary dengan struktur:
    - version
    - model_name
    - model
    - feature_columns
    - target column
    - results
    """

    def __init__(self, model_path: str = "models/stock_model_v1.0.1.pkl"):
        self.model_path = Path(model_path)
        self.model_bundle: Optional[Dict[str, Any]] = None
        self.model: Optional[Any] = None
        self.feature_columns: Optional[List[str]] = None
        self.version: Optional[str] = None
        self.model_name: Optional[str] = None
        self.target_column: Optional[str] = None
        self.results: Optional[Dict[str, Any]] = None
        self.classes: Optional[List[str]] = None
        self.is_loaded: bool = False

    def load_model(self) -> None:
        """
        Load model dari file .pkl dan validasi struktur dasarnya.
        """

        if not self.model_path.exists():
            raise ModelLoaderError(f"File model tidak ditemukan: {self.model_path}")
        
        loaded_object = joblib.load(self.model_path)

        if not isinstance(loaded_object, dict):
            raise ModelLoaderError(
                "Format model tidak valid. File .pkl seharusnya berisi dictionary."
            )
        
        required_keys = [
            "version",
            "model_name",
            "model",
            "feature_columns",
            "target_column",
            "results",
        ]

        missing_keys = [
            key for key in required_keys if key not in loaded_object
        ]

        if missing_keys:
            raise ModelLoaderError(
                f"Model bundle tidak lengkap. Key yang hilang: {missing_keys}"
            )
        
        model = loaded_object["model"]
        feature_columns = loaded_object["feature_columns"]

        if not hasattr(model, "predict"):
            raise ModelLoaderError(
                "Object pada key 'model' tidak memiliki method predict()."
            )
        
        if not isinstance(feature_columns, list):
            raise ModelLoaderError(
                "Object pada key 'feature_columns' harus berupa list."
            )
        
        self.model_bundle = loaded_object
        self.model = model
        self.feature_columns = feature_columns
        self.version = loaded_object["version"]
        self.model_name = loaded_object["model_name"]
        self.target_column = loaded_object["target_column"]
        self.results = loaded_object["results"]
        self.classes = self._get_model_classes()
        self.is_loaded = True

    def _get_model_classes(self) -> Optional[List[str]]:
        """
        Mengambil urutan class dari model.
        Ini penting untuk membaca hasil predict_proba().
        """

        if self.model is None:
            return None
        
        if hasattr(self.model, "classes_"):
            return list(self.model.classes_)
        
        if hasattr(self.model, "named_steps"):
            steps = list(self.model.named_steps.values())

            for _, step in reversed(steps):
                if hasattr(step, "classes_"):
                    return list(step.classes_)
                
        return None

    def ensure_model_loaded(self) -> None:
        """
        Memastikan model sudah di-load.
        Kalau belum, model akan di-load secara lazy.
        """

        if not self.is_loaded:
            self.load_model()

    def get_model_info(self) -> Dict[str,Any]:
        """
        Mengambil informasi model untuk endpoint /model-info.
        """

        self.ensure_model_loaded()

        return {
            "is_loaded": self.is_loaded,
            "model_path": str(self.model_path),
            "version": self.version,
            "model_name": self.model_name,
            "target_column": self.target_column,
            "feature_columns": self.feature_columns,
            "classes": self.classes,
            "results": self.results,
        }

    def predict(self, input_data: Dict[str, float]) -> Dict[str, Any]:
        """
        Melakukan prediksi berdasarkan input dictionary.
        
        Method ini akan dipakai penuh pada Tahap 3.
        Pada Tahap 2, method ini disiapkan dulu agar service lengkap.
        """

        self.ensure_model_loaded()

        if self.model is None:
            raise ModelLoaderError("Model belum berhasil di-load.")
        
        if self.feature_columns is None:
            raise ModelLoaderError("Feature columns belum tersedia.")
        
        missing_features = [
            feature for feature in self.feature_columns if feature not in input_data
        ]

        if missing_features:
            raise ModelLoaderError(
                f"Input data tidak lengkap. Feature yang hilang: {missing_features}"
            )
        
        ordered_input = {
            feature: input_data[feature] for feature in self.feature_columns
        }

        input_df = pd.DataFrame([ordered_input])

        prediction = self.model.predict(input_df)[0]

        response = {
            "prediction": prediction,
            "confidence": None,
            "probabilities": None,
        }

        if hasattr(self.model, "predict_proba"):
            probabilities = self.model.predict_proba(input_df)[0]

            if self.classes is not None:
                probability_dict = {
                    str(label): float(prob)
                    for label, prob in zip(self.classes, probabilities)
                }
            else:
                probability_dict = {
                    str(index): float(prob)
                    for index, prob in enumerate(probabilities)
                }
            
            response["probabilities"] = probability_dict
            response["confidence"] = float(max(probabilities))

        return response
    
model_loader = StockModelLoader()