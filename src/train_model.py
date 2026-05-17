"""
train_model.py

Modul ini digunakan untuk melatih model machine learning
untuk merekomendasikan saham Buy, Hold, atau Sell.

Input:
- data/processed/{ticket}_labeled.csv

Output:
- model/stock_model_v1.0.1.pkl
"""

from pathlib import Path
from typing import Dict, Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

FEATURE_COLUMNS = ["Daily_Return", "MA_5", "MA_10", "RSI", "Volatility", "Volume_Change"]

TARGET_COLUMN = "Recommendation"

VERSION = "v1.0.1"

def load_labeled_data(input_path: str) -> pd.DataFrame:
    """
    Membaca data saham yang sudah memiliki fitur dan label.

    Parameters
    ----------
    input_path : str
        Lokasi file CSV data berlabel.

    Returns
    -------
    pd.DataFrame
        DataFrame berisi data fitur dan label.
    """

    input_file = Path(input_path)

    if not input_file.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {input_path}")
    
    print(f"Membaca data berlabel dari: {input_path}")

    data = pd.read_csv(input_file)

    required_columns = FEATURE_COLUMNS + [TARGET_COLUMN, "Date"]

    missing_columns = set(required_columns) - set(data.columns)

    if missing_columns:
        raise ValueError(f"Kolom wajib tidak ditemukan: {missing_columns}")
    
    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
    data = data.sort_values(by="Date").reset_index(drop=True)

    # Pastikan semua fitur berbentuk angka
    for column in FEATURE_COLUMNS:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    # Ganti nilai infinity menjadi NaN
    data[FEATURE_COLUMNS] = data[FEATURE_COLUMNS].replace(
        [np.inf, -np.inf],
        np.nan,
    )

    # Hapus data yang masih memiliki NaN setelah pembersihan
    before_cleaning = len(data)
    data = data.dropna(subset=required_columns).reset_index(drop=True)
    after_cleaning = len(data)

    removed_rows = before_cleaning - after_cleaning

    print(f"Jumlah data siap training: {len(data)} baris")
    print(f"Jumlah baris dihapus karena NaN/Infinity: {removed_rows}")

    return data

def time_based_train_test_split(
    data: pd.DataFrame,
    test_size: float = 0.2,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Membagi data menjadi training dan testing berdasarkan rurtan waktu.
    
    Data lama digunakan untuk training.
    Data terbaru digunakan untuk testing.
    
    Parameters
    ----------
    data : pd.DataFrame
        DataFrame berisi fitur dan target.

    test_size : float
        Persentase data untuk testing.
        Default 0.2 berarti 20% data terbaru untuk testing.

    Returns
    -------
    X_train, X_test, y_train, y_test
    """

    if not 0 < test_size < 1:
        raise ValueError("test_size harus di antara 0 dan 1.")
    
    split_index = int(len(data) * (1 - test_size))

    if split_index <= 0 or split_index >= len(data):
        raise ValueError("Ukuran data tidak cukup untuk train-test split.")
    
    train_data = data.iloc[:split_index].copy()
    test_data = data.iloc[split_index:].copy()

    X_train = train_data[FEATURE_COLUMNS]
    y_train = train_data[TARGET_COLUMN]

    X_test = test_data[FEATURE_COLUMNS]
    y_test = test_data[TARGET_COLUMN]

    print("\nPembagian data berdasarkan waktu:")
    print(f"Training data : {len(X_train)} baris")
    print(f"Testing data : {len(X_test)} baris")

    print("\nPeriode training:")
    print(f"{train_data['Date'].min().date()} sampai {train_data['Date'].max().date()}")

    print("\nPeriode testing:")
    print(f"{test_data['Date'].min().date()} sampai {test_data['Date'].max().date()}")

    return X_train, X_test, y_train, y_test

def build_models() -> Dict[str, Pipeline]:
    """
    Membuat daftar model baseline yang akan dilatih.
    
    Returns
    -------
    Dict[str, Pipeline]
        Dictionary berisi nama model dan pipeline model.
    """

    models = {
        "Logistic Regression": Pipeline(
            steps=[
                ("scaler", StandardScaler()),
                (
                    "model",
                    LogisticRegression(
                        max_iter=1000,
                        class_weight="balanced",
                        random_state=42,
                    ),
                ),
            ]
        ),
        "Random Forest": Pipeline(
            steps=[
                (
                    "model",
                    RandomForestClassifier(
                        n_estimators=200,
                        max_depth=None,
                        class_weight="balanced",
                        random_state=42,
                    ),
                ),
            ]
        ),
    }

    return models

def train_and_compare_models(
    X_train: pd.DataFrame,
    X_test: pd.Series,
    y_train: pd.Series,
    y_test: pd.Series,
) -> Tuple[str, Pipeline, Dict]:
    """
    Melatih beberapa model dan memilih model terbaik berdasarkan macro F1-score.
    
    Parameters
    ----------
    X_train : pd.DataFrame
        Fitur training.
        
    X_test : pd.DataFrame
        Fitur testing.
        
    y_train : pd.Series
        Target training.
        
    y_test : pd.Series
        Target testing.

    Returns
    -------
    best_model_name : str
        Nama model terbaik.
        
    best_model : Pipeline
        Model terbaik yang sudah dilatih.
        
    results : Dict
        Hasil evaluasi semua model.
    """

    models = build_models()
    results = {}

    best_model_name = None
    best_model = None
    best_f1_score = -1

    for model_name, model in models.items():
        print("\n" + "=" * 50)
        print(f"Training model: {model_name}")
        print("=" * 50)

        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        macro_f1 = f1_score(y_test, y_pred, average="macro", zero_division=0)

        report = classification_report(
            y_test,
            y_pred,
            zero_division=0,
            output_dict=True,
        )

        results[model_name] = {
            "accuracy": accuracy,
            "macro_f1": macro_f1,
            "classification_report": report,
        }

        print(f"Accuracy : {accuracy:.4f}")
        print(f"Macro F1 : {macro_f1:.4f}")

        print("\nClassification Report:")
        print(
            classification_report(
                y_test,
                y_pred,
                zero_division=0,
            )
        )

        if macro_f1 > best_f1_score:
            best_f1_score = macro_f1
            best_model_name = model_name
            best_model = model

    print("\n" + "=" * 50)
    print("Model terbaik")
    print("=" * 50)
    print(f"Model    : {best_model_name}")
    print(f"Macro F1 : {best_f1_score:.4f}")

    return best_model_name, best_model, results

def save_model(
    model: Pipeline,
    model_name: str,
    results: Dict,
    output_path: str = "model/stock_model_v1.0.1.pkl",
) -> None:
    """
    Menyimpan model terbaik ke file .pkl.
    
    Parameters
    ----------
    model : Pipeline
        Model terbaik yang sudah dilatih.

    model_name : str
        Nama model terbaik.

    results : Dict
        Hasil evaluasi semua model.
    
    output_path : str
        Lokasi file output model.
    """

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    model_package = {
        "version": VERSION,
        "model_name": model_name,
        "model": model,
        "feature_columns": FEATURE_COLUMNS,
        "target_column": TARGET_COLUMN,
        "results": results,
    }

    joblib.dump(model_package, output_file)

    print(f"\nModel terbaik disimpan ke: {output_file}")


def train_model(
    input_path: str,
    model_output_path: str = "model/stock_model_v1.0.1.pkl",
    test_size: float = 0.2,
) -> Dict:
    """
    Fungsi utama untuk menjalankan proses training model.
    
    Parameters
    ----------
    input_path : str
        Lokasi file CSV data berlabel.

    model_output_path : str
        Lokasi output model .pkl.

    test_size : float
        Persentase data testing.

    Returns
    -------
    Dict
        informasi model terbaik dan hasil evaluasi.
    """

    data = load_labeled_data(input_path=input_path)

    print("\nDistribusi label seluruh data:")
    print(data[TARGET_COLUMN].value_counts())

    X_train, X_test, y_train, y_test = time_based_train_test_split(
        data=data,
        test_size=test_size,
    )

    print("\nDistribusi label data training:")
    print(y_train.value_counts())

    print("\nDistribusi label data testing:")
    print(y_test.value_counts())

    best_model_name, best_model, results = train_and_compare_models(
        X_train=X_train,
        X_test=X_test,
        y_train=y_train,
        y_test=y_test,
    )

    save_model(
        model=best_model,
        model_name=best_model_name,
        results=results,
        output_path=model_output_path,
    )

    training_summary = {
        "version": VERSION,
        "best_model_name": best_model_name,
        "model_output_path": model_output_path,
        "feature_columns": FEATURE_COLUMNS,
        "target_column": TARGET_COLUMN,
        "results": results,
    }

    return training_summary

if __name__ == "__main__":
    summary = train_model(
        input_path="data/processed/BBCA_JK_labeled.csv",
        model_output_path="models/stock_model_v1.0.1.pkl",
        test_size=0.2,
    )

    print("\nTraining selesai")
    print(f"Model terbaik: {summary['best_model_name']}")