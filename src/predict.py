"""
predict.py

Modul untuk melakukan prediksi rekomendasi saham menggunakan model yang sudah dilatih.

Input:
- models/stock_model_v1.0.1.pkl
- data/processed/BBCA_JK_features.csv

Output:
- Rekomendasi terbaru: Buy, Hold, atau Sell
- reports/prediction_v1.0.1.md
"""

from pathlib import Path
from typing import Dict

import joblib
import numpy as np
import pandas as pd

def load_model(model_path: str) -> Dict:
    """
    Membaca model yang sudah disimpan dalam file .pkl.
    """
    
    model_file = Path(model_path)

    if not model_file.exists():
        raise FileNotFoundError(f"File model tidak ditemukan: {model_file}")
    
    print(f"Membaca model dari: {model_path}")

    model_package = joblib.load(model_file)

    required_keys = [
        "version",
        "model_name",
        "model",
        "feature_columns",
        "target_column",
    ]

    missing_keys = set(required_keys) - set(model_package.keys())

    if missing_keys:
        raise ValueError(f"Model package tidak lengkap. Key hilang: {missing_keys}")
    
    return model_package

def load_feature_data(
    feature_data_path: str,
    feature_columns: list,
) -> pd.DataFrame:
    """
    Membaca data fitur yang akan digunakan untuk prediksi.
    """

    feature_file = Path(feature_data_path)

    if not feature_file.exists():
        raise FileNotFoundError(f"File data fitur tidak ditemukan: {feature_data_path}")

    print(f"Membaca data fitur dari: {feature_data_path}")

    data = pd.read_csv(feature_file)

    required_columns = ["Date"] + feature_columns

    missing_columns = set(required_columns) - set(data.columns)

    if missing_columns:
        raise ValueError(f"Kolom wajib tidak ditemukan: {missing_columns}")
    
    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
    data = data.sort_values(by="Date").reset_index(drop=True)

    for column in feature_columns:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    data[feature_columns] = data[feature_columns].replace(
        [np.inf, -np.inf],
        np.nan,
    )

    before_cleaning = len(data)
    data = data.dropna(subset=required_columns).reset_index(drop=True)
    after_cleaning = len(data)

    removed_rows = before_cleaning - after_cleaning

    print(f"Jumlah data siap prediksi: {after_cleaning} baris")
    print(f"Jumlah baris dihapus karena NaN/Infinity: {removed_rows}")
    
    if data.empty:
        raise ValueError("Data kosong setelah proses cleaning. Prediksi tidak bisa dilakukan")
    
    return data

def get_latest_data(
        data: pd.DataFrame,
        feature_columns: list,
) -> tuple[pd.DataFrame, pd.Series]:
    """
    Mengambil baris data terbaru untuk diprediksi.
    """
    
    latest_row = data.iloc[-1].copy()
    X_latest = latest_row[feature_columns].to_frame().T

    return X_latest, latest_row

def predict_recommendation(
    model_package: Dict,
    feature_data_path: str,
) -> Dict:
    """
    Melakukan prediksi rekomendasi saham terbaru.
    """

    model = model_package["model"]
    model_version = model_package["version"]
    model_name = model_package["model_name"]
    feature_columns = model_package["feature_columns"]

    data = load_feature_data(
        feature_data_path=feature_data_path,
        feature_columns=feature_columns,
    )

    X_latest, latest_row = get_latest_data(
        data=data,
        feature_columns=feature_columns,
    )

    prediction = model.predict(X_latest)[0]

    probability_result = None
    
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(X_latest)[0]
        classes = model.classes_

        probability_result = {
            class_name: probability
            for class_name, probability in zip(classes, probabilities)
        }

    prediction_result = {
        "version": model_version,
        "model_name": model_name,
        "date": latest_row["Date"],
        "recommendation": prediction,
        "latest_close": latest_row.get("Close", None),
        "features": latest_row[feature_columns].to_dict(),
        "probabilities": probability_result,
    }
    
    return prediction_result

def save_prediction_report(
    prediction_result: Dict,
    output_path: str = "reports/prediction_v1.0.1.md",
) -> None:
    """
    Menyimpan hasil prediksi ke file Markdown.
    """

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    feature_series = pd.Series(prediction_result["features"])

    if prediction_result["probabilities"] is not None:
        probability_series = pd.Series(prediction_result["probabilities"])
        probability_text = probability_series.to_markdown()
    else:
        probability_text = "Model tidak menyediakan nilai probabilitas."

    latest_close = prediction_result["latest_close"]

    if latest_close is None:
        latest_close_text = "-"
    else:
        latest_close_text = f"{latest_close:.2f}"

    report_text = f"""# Prediction Report - Stock Recommendation ML {prediction_result["version"]}

## 1. Ringkasan Prediksi

| Item | Keterangan |
|---|---|
| Version | {prediction_result["version"]} |
| Model | {prediction_result["model_name"]} |
| Tanggal data terbaru | {prediction_result["date"].date()} |
| Harga Close terbaru | {latest_close_text} |
| Rekomendasi model | {prediction_result["recommendation"]} |

## 2. Probabilitas Prediksi

{probability_text}

## 3. Fitur yang Digunakan

{feature_series.to_markdown()}

## 4. Catatan Penting

Hasil prediksi ini hanya digunakan untuk pembelajaran dan portofolio machine learning.

Output Buy, Hold, atau Sell dari model ini **bukan nasihat investasi**.

Model v1.0.1 masih merupakan baseline awal, sehingga hasil prediksi harus dipahami sebagai eksperimen machine learning, bukan rekomendasi finansial nyata.
"""
    
    output_file.write_text(report_text, encoding="utf-8")

    print(f"\nLaporan prediksi berhasil disimpan ke: {output_file}")

def run_prediction(
    model_path: str = "models/stock_model_v1.0.1.pkl",
    feature_data_path: str = "data/processed/BBCA_JK_features.csv",
    report_output_path: str = "reports/prediction_v1.0.1.md",
) -> Dict:
    """
    Fungsi utama untuk menjalankan prediksi.
    """

    model_package = load_model(model_path=model_path)

    prediction_result = predict_recommendation(
        model_package=model_package,
        feature_data_path=feature_data_path,
    )

    print("\nHasil Prediksi Terbaru")
    print("=" * 50)
    print(f"Version        : {prediction_result['version']}")
    print(f"Model          : {prediction_result['model_name']}")
    print(f"Tanggal data   : {prediction_result['date'].date()}")
    print(f"Close terbaru  : {prediction_result['latest_close']}")
    print(f"Rekomendasi    : {prediction_result['recommendation']}")

    if prediction_result["probabilities"] is not None:
        print("\nProbabilitas:")
        for label, probability in prediction_result["probabilities"].items():
            print(f"{label}: {probability:.4f}")

    save_prediction_report(
        prediction_result=prediction_result,
        output_path=report_output_path,
    )

    return prediction_result

if __name__ == "__main__":
    result = run_prediction()

    print("\nPrediksi selesai.")
    print(f"Rekomendasi terbaru: {result['recommendation']}")