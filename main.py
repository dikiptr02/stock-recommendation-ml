"""
main.py

Pipeline utama project Stock Recommendation ML v1.0.1.

Tahap yang sudah berjalan:
1. Data Collection: Mengambil data historis saham menggunakan yfinance.
2. Data Preprocessing: Membersihkan data historis saham.
3. Feature Engineering: Membuat fitur machine learning dari data historis saham yang sudah dibersihkan.
4. Labeling: Membuat label Buy, Hold, Sell berdasarkan return masa depan.
5. Training Model: Melatih model machine learning untuk merekomendasikan saham Buy, Hold, atau Sell.
6. Evaluation Model: Mengevaluasi performa model menggunakan metrik akurasi, precision, recall, dan F1-score.
"""

from src.data_collection import download_stock_data
from src.preprocessing import preprocess_stock_data
from src.feature_engineering import create_features
from src.labeling import create_labels
from src.train_model import train_model
from src.evaluate_model import evaluate_model


def main() -> None:
    """
    Fungsi utama untuk menjalankan pipeline project.
    """
    
    ticker = "BBCA.JK"
    star_date = "2018-01-01"
    end_date = None

    print("=" * 50)
    print("STOCK RECOMMENDATION ML - v1.0.1")
    print("=" * 50)

    clean_ticker_name = ticker.replace(".", "_")

    raw_file_path = f"data/raw/{clean_ticker_name}_raw.csv"
    clean_file_path = f"data/processed/{clean_ticker_name}_clean.csv"
    features_file_path = f"data/processed/{clean_ticker_name}_features.csv"
    labeled_file_path = f"data/processed/{clean_ticker_name}_labeled.csv"
    model_output_path = "models/stock_model_v1.0.1.pkl"
    report_output_path = "reports/evaluation_v1.0.1.md"

    print("\n[1] Data Collection")
    raw_data = download_stock_data(
        ticker=ticker,
        start_date=star_date,
        end_date=end_date,
        output_dir="data/raw",
    )

    print("\nPreview data mentah:")
    print(raw_data.head())

    print("\n[2] Data Preprocessing")
    clean_data = preprocess_stock_data(
        input_path=raw_file_path,
        output_dir="data/processed",
    )

    print("\nPreview data bersih:")
    print(clean_data.head())

    print("\n[3] Feature Engineering")
    feature_data = create_features(
        input_path=clean_file_path,
        output_dir="data/processed",
    )

    print("\nPreview data dengan fitur:")
    print(feature_data.head())

    print("\n[4] Labeling")
    labeled_data = create_labels(
        input_path=features_file_path,
        output_dir="data/processed",
        horizon=5,
        buy_threshold=0.02,
        sell_threshold=-0.02,
    )

    print("\nPreview data berlabel:")
    print(labeled_data.head())

    print("\n[5] Training Model")
    training_summary = train_model(
        input_path=labeled_file_path,
        model_output_path=model_output_path,
        test_size=0.2,
    )

    print("\nRingkasan training:")
    print(f"Version          : {training_summary['version']}")
    print(f"Model terbaik    : {training_summary['best_model_name']}")
    print(f"Model disimpan di: {training_summary['model_output_path']}")

    print("\n[6] Evaluation Model")
    evaluation_results = evaluate_model(
        data_path=labeled_file_path,
        model_path=model_output_path,
        report_output_path=report_output_path,
        test_size=0.2,
    )

    print("\nRingkasan evaluasi:")
    print(f"Accuracy : {evaluation_results['accuracy']:.4f}")
    print(f"F1 Macro : {evaluation_results['f1_macro']:.4f}")

    print("\nPipeline berhasil dijalankan.")


if __name__ == "__main__":
    main()