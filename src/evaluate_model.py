"""
evaluate_model.py

Modul untuk mengevaluasi model machine learning rekomendasi saham.

Input:
- data/processed/BBCA_JK_labeled.csv
- models/stock_model_v1.0.1.pkl

Output:
- reports/evaluation_v1.0.1.md
"""

from pathlib import Path
from typing import Dict, Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)


def load_model(model_path: str) -> Dict:
    """
    Membaca model yang sudah disimpan dalam file .pkl.
    """

    model_file = Path(model_path)

    if not model_file.exists():
        raise FileNotFoundError(f"File model tidak ditemukan: {model_path}")

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


def load_data(
    data_path: str,
    feature_columns: list,
    target_column: str,
) -> pd.DataFrame:
    """
    Membaca data labeled dan membersihkan nilai NaN/Infinity.
    """

    data_file = Path(data_path)

    if not data_file.exists():
        raise FileNotFoundError(f"File data tidak ditemukan: {data_path}")

    print(f"Membaca data dari: {data_path}")

    data = pd.read_csv(data_file)

    required_columns = ["Date"] + feature_columns + [target_column]

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

    print(f"Jumlah data siap evaluasi: {after_cleaning} baris")
    print(f"Jumlah baris dihapus karena NaN/Infinity: {removed_rows}")

    return data


def split_data_by_time(
    data: pd.DataFrame,
    feature_columns: list,
    target_column: str,
    test_size: float = 0.2,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.Series]:
    """
    Membagi data berdasarkan waktu.

    Data lama digunakan sebagai training.
    Data terbaru digunakan sebagai testing.
    """

    if not 0 < test_size < 1:
        raise ValueError("test_size harus lebih dari 0 dan kurang dari 1.")

    split_index = int(len(data) * (1 - test_size))

    if split_index <= 0 or split_index >= len(data):
        raise ValueError("Ukuran data tidak cukup untuk train-test split.")

    train_data = data.iloc[:split_index].copy()
    test_data = data.iloc[split_index:].copy()

    X_test = test_data[feature_columns]
    y_test = test_data[target_column]

    print("\nPembagian data evaluasi:")
    print(f"Training data : {len(train_data)} baris")
    print(f"Testing data  : {len(test_data)} baris")

    print("\nPeriode training:")
    print(f"{train_data['Date'].min().date()} sampai {train_data['Date'].max().date()}")

    print("\nPeriode testing:")
    print(f"{test_data['Date'].min().date()} sampai {test_data['Date'].max().date()}")

    return train_data, test_data, X_test, y_test


def calculate_metrics(
    y_test: pd.Series,
    y_pred: np.ndarray,
) -> Dict:
    """
    Menghitung metrik evaluasi model.
    """

    labels = ["Buy", "Hold", "Sell"]

    accuracy = accuracy_score(y_test, y_pred)

    precision_macro = precision_score(
        y_test,
        y_pred,
        average="macro",
        zero_division=0,
    )

    recall_macro = recall_score(
        y_test,
        y_pred,
        average="macro",
        zero_division=0,
    )

    f1_macro = f1_score(
        y_test,
        y_pred,
        average="macro",
        zero_division=0,
    )

    precision_weighted = precision_score(
        y_test,
        y_pred,
        average="weighted",
        zero_division=0,
    )

    recall_weighted = recall_score(
        y_test,
        y_pred,
        average="weighted",
        zero_division=0,
    )

    f1_weighted = f1_score(
        y_test,
        y_pred,
        average="weighted",
        zero_division=0,
    )

    classification_report_text = classification_report(
        y_test,
        y_pred,
        labels=labels,
        zero_division=0,
    )

    confusion_matrix_array = confusion_matrix(
        y_test,
        y_pred,
        labels=labels,
    )

    confusion_matrix_df = pd.DataFrame(
        confusion_matrix_array,
        index=[f"Actual {label}" for label in labels],
        columns=[f"Predicted {label}" for label in labels],
    )

    results = {
        "accuracy": accuracy,
        "precision_macro": precision_macro,
        "recall_macro": recall_macro,
        "f1_macro": f1_macro,
        "precision_weighted": precision_weighted,
        "recall_weighted": recall_weighted,
        "f1_weighted": f1_weighted,
        "classification_report": classification_report_text,
        "confusion_matrix": confusion_matrix_df,
    }

    return results


def save_evaluation_report(
    output_path: str,
    model_version: str,
    model_name: str,
    feature_columns: list,
    target_column: str,
    train_data: pd.DataFrame,
    test_data: pd.DataFrame,
    y_test: pd.Series,
    y_pred: np.ndarray,
    results: Dict,
) -> None:
    """
    Menyimpan laporan evaluasi dalam format Markdown.
    """

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    actual_distribution = y_test.value_counts()
    prediction_distribution = pd.Series(y_pred).value_counts()

    feature_text = "\n".join([f"- {feature}" for feature in feature_columns])

    report_text = f"""# Evaluation Report - Stock Recommendation ML {model_version}

## 1. Ringkasan Model

| Item | Keterangan |
|---|---|
| Version | {model_version} |
| Model terbaik | {model_name} |
| Target | {target_column} |
| Jumlah fitur | {len(feature_columns)} |

## 2. Fitur yang Digunakan

{feature_text}

## 3. Pembagian Data

Data dibagi menggunakan **time-based split**, yaitu data lama sebagai training dan data terbaru sebagai testing.

| Dataset | Jumlah Data | Periode |
|---|---:|---|
| Training | {len(train_data)} | {train_data["Date"].min().date()} sampai {train_data["Date"].max().date()} |
| Testing | {len(test_data)} | {test_data["Date"].min().date()} sampai {test_data["Date"].max().date()} |

## 4. Distribusi Label Aktual pada Data Testing

{actual_distribution.to_markdown()}

## 5. Distribusi Prediksi Model pada Data Testing

{prediction_distribution.to_markdown()}

## 6. Evaluation Metrics

| Metric | Score |
|---|---:|
| Accuracy | {results["accuracy"]:.4f} |
| Precision Macro | {results["precision_macro"]:.4f} |
| Recall Macro | {results["recall_macro"]:.4f} |
| F1 Macro | {results["f1_macro"]:.4f} |
| Precision Weighted | {results["precision_weighted"]:.4f} |
| Recall Weighted | {results["recall_weighted"]:.4f} |
| F1 Weighted | {results["f1_weighted"]:.4f} |

## 7. Classification Report

{results["classification_report"]}

## 8. Confusion Matrix

{results["confusion_matrix"].to_markdown()}

## 9. Interpretasi Singkat

Model ini adalah baseline awal untuk project pembelajaran dan portofolio.

Catatan penting:

- Accuracy tidak cukup untuk menilai model.
- Macro F1-score penting karena kelas Buy, Hold, dan Sell bisa tidak seimbang.
- Confusion matrix digunakan untuk melihat kesalahan prediksi tiap kelas.
- Model ini belum boleh digunakan sebagai nasihat investasi nyata.

## 10. Keterbatasan Model v1.0.1

- Fitur masih sederhana.
- Belum ada hyperparameter tuning.
- Belum ada walk-forward validation.
- Belum ada backtesting.
- Belum memperhitungkan biaya transaksi.
- Belum menggunakan data fundamental.
- Belum menggunakan data sentimen berita.

## 11. Disclaimer

Project ini hanya untuk pembelajaran dan portofolio data science/machine learning.

Output model bukan nasihat investasi.
"""

    output_file.write_text(report_text, encoding="utf-8")

    print(f"\nLaporan evaluasi berhasil disimpan ke: {output_file}")


def evaluate_model(
    data_path: str = "data/processed/BBCA_JK_labeled.csv",
    model_path: str = "models/stock_model_v1.0.1.pkl",
    report_output_path: str = "reports/evaluation_v1.0.1.md",
    test_size: float = 0.2,
) -> Dict:
    """
    Fungsi utama untuk evaluasi model.
    """

    model_package = load_model(model_path)

    model_version = model_package["version"]
    model_name = model_package["model_name"]
    model = model_package["model"]
    feature_columns = model_package["feature_columns"]
    target_column = model_package["target_column"]

    data = load_data(
        data_path=data_path,
        feature_columns=feature_columns,
        target_column=target_column,
    )

    train_data, test_data, X_test, y_test = split_data_by_time(
        data=data,
        feature_columns=feature_columns,
        target_column=target_column,
        test_size=test_size,
    )

    print("\nMelakukan prediksi pada data testing...")

    y_pred = model.predict(X_test)

    results = calculate_metrics(
        y_test=y_test,
        y_pred=y_pred,
    )

    print("\nHasil Evaluasi:")
    print(f"Accuracy        : {results['accuracy']:.4f}")
    print(f"Precision Macro : {results['precision_macro']:.4f}")
    print(f"Recall Macro    : {results['recall_macro']:.4f}")
    print(f"F1 Macro        : {results['f1_macro']:.4f}")

    print("\nClassification Report:")
    print(results["classification_report"])

    print("\nConfusion Matrix:")
    print(results["confusion_matrix"])

    save_evaluation_report(
        output_path=report_output_path,
        model_version=model_version,
        model_name=model_name,
        feature_columns=feature_columns,
        target_column=target_column,
        train_data=train_data,
        test_data=test_data,
        y_test=y_test,
        y_pred=y_pred,
        results=results,
    )

    return results


if __name__ == "__main__":
    evaluation_results = evaluate_model()

    print("\nEvaluasi selesai.")
    print(f"F1 Macro: {evaluation_results['f1_macro']:.4f}")