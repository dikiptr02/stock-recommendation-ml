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
        # Menyimpan path lokasi file model
        self.model_path = Path(model_path)
        
        # Variabel untuk menampung seluruh isi file .pkl
        self.model_bundle: Optional[Dict[str, Any]] = None
        
        # Variabel untuk menampung objek algoritma machine learning (misal: RandomForest)
        self.model: Optional[Any] = None
        
        # Variabel untuk menyimpan urutan kolom fitur yang diminta model
        self.feature_columns: Optional[List[str]] = None
        
        # Metadata pendukung model
        self.version: Optional[str] = None
        self.model_name: Optional[str] = None
        self.target_column: Optional[str] = None
        self.results: Optional[Dict[str, Any]] = None
        self.classes: Optional[List[str]] = None
        
        # Penanda apakah model sudah berhasil diload ke memory
        self.is_loaded: bool = False

    def load_model(self) -> None:
        """
        Load model dari file .pkl dan validasi struktur dasarnya.
        """

        # Mengecek keberadaan file secara fisik
        if not self.model_path.exists():
            raise ModelLoaderError(f"File model tidak ditemukan: {self.model_path}")
        
        # Memuat isi file pkl (deserialize)
        loaded_object = joblib.load(self.model_path)

        # Memastikan struktur dasar file yang diload adalah dictionary
        if not isinstance(loaded_object, dict):
            raise ModelLoaderError(
                "Format model tidak valid. File .pkl seharusnya berisi dictionary."
            )
        
        # Daftar key yang mutlak wajib ada dalam dictionary model
        required_keys = [
            "version",
            "model_name",
            "model",
            "feature_columns",
            "target_column",
            "results",
        ]

        # Mengecek apakah ada key wajib yang hilang
        missing_keys = [
            key for key in required_keys if key not in loaded_object
        ]

        # Batalkan load dan lemparkan error jika file tidak lengkap
        if missing_keys:
            raise ModelLoaderError(
                f"Model bundle tidak lengkap. Key yang hilang: {missing_keys}"
            )
        
        # Mengekstrak komponen algoritma ML dan kolom fiturnya
        model = loaded_object["model"]
        feature_columns = loaded_object["feature_columns"]

        # Validasi keamanan: Pastikan model ML tersebut bisa digunakan untuk prediksi
        if not hasattr(model, "predict"):
            raise ModelLoaderError(
                "Object pada key 'model' tidak memiliki method predict()."
            )
        
        # Validasi keamanan: Pastikan daftar kolom berbentuk list
        if not isinstance(feature_columns, list):
            raise ModelLoaderError(
                "Object pada key 'feature_columns' harus berupa list."
            )
        
        # Menyimpan semuanya ke atribut class agar bisa digunakan secara global
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
        Ini penting untuk membaca hasil predict_proba() secara akurat.
        """

        # Jika model belum diload, abaikan
        if self.model is None:
            return None
        
        # Mengecek atribut classes_ yang umum ada di scikit-learn
        if hasattr(self.model, "classes_"):
            return list(self.model.classes_)
        
        # Jika model adalah pipeline, cari dari langkah-langkah di dalamnya (secara mundur)
        if hasattr(self.model, "named_steps"):
            steps = list(self.model.named_steps.values())

            for _, step in reversed(steps):
                if hasattr(step, "classes_"):
                    return list(step.classes_)
                
        return None

    def ensure_model_loaded(self) -> None:
        """
        Memastikan model sudah di-load.
        Kalau belum, model akan di-load secara lazy (tepat sebelum prediksi).
        """

        if not self.is_loaded:
            self.load_model()

    def get_model_info(self) -> Dict[str,Any]:
        """
        Mengambil informasi model untuk disajikan di endpoint /model-info.
        """

        # Pastikan model di-load terlebih dahulu
        self.ensure_model_loaded()

        # Menyusun ringkasan metadata model
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
        Melakukan prediksi klasifikasi (Buy/Hold/Sell) berdasarkan input JSON.
        """

        # Pastikan model diload tepat sebelum prediksi dilakukan
        self.ensure_model_loaded()

        # Verifikasi kelengkapan objek model
        if self.model is None:
            raise ModelLoaderError("Model belum berhasil di-load.")
        
        # Verifikasi kelengkapan daftar fitur
        if self.feature_columns is None:
            raise ModelLoaderError("Feature columns belum tersedia.")
        
        # Mengecek apakah user menginput semua nilai fitur yang dibutuhkan model
        missing_features = [
            feature for feature in self.feature_columns if feature not in input_data
        ]

        if missing_features:
            raise ModelLoaderError(
                f"Input data tidak lengkap. Feature yang hilang: {missing_features}"
            )
        
        # Mengatur urutan input persis seperti urutan saat model dilatih
        ordered_input = {
            feature: input_data[feature] for feature in self.feature_columns
        }

        # Mengubah data dari list of dict ke bentuk Pandas DataFrame agar sesuai input scikit-learn
        input_df = pd.DataFrame([ordered_input])

        # Mengeksekusi prediksi dari algoritma ML
        prediction = self.model.predict(input_df)[0]

        # Struktur respons standar
        response = {
            "prediction": str(prediction),
            "confidence": None,
            "probabilities": None,
        }

        # Jika model punya kapabilitas menebak probabilitas (seperti Random Forest)
        if hasattr(self.model, "predict_proba"):
            # Menarik daftar probabilitas tiap kelas
            probabilities = self.model.predict_proba(input_df)[0]

            # Menggabungkan nama kelas dengan nilai probabilitasnya
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
            
            # Melampirkan persentase ke dalam response akhir
            response["probabilities"] = probability_dict
            response["confidence"] = float(max(probabilities))

        return response
    
# Instance tunggal (singleton) agar model cukup diload sekali selama server menyala
model_loader = StockModelLoader()