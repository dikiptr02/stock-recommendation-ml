"""
main.py

Pipeline utama project Stock Recommendation ML v1.0.1.

Tahap yang sudah berjalan:
1. Data Collection: Mengambil data historis saham menggunakan yfinance.
2. Data Preprocessing: Membersihkan data historis saham.
3. Feature Engineering: Membuat fitur machine learning dari data historis saham yang sudah dibersihkan.
"""

from src.data_collection import download_stock_data
from src.preprocessing import preprocess_stock_data
from src.feature_engineering import create_features


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

    print("\n[1] Data Collection")
    raw_data = download_stock_data(
        ticker=ticker,
        start_date=star_date,
        end_date=end_date,
        output_dir="data/raw",
    )

    print("\nPreview data mentah:")
    print(raw_data.head())

    clean_ticker_name = ticker.replace(".", "_")
    raw_file_path = f"data/raw/{clean_ticker_name}_raw.csv"
    clean_file_path = f"data/processed/{clean_ticker_name}_clean.csv"

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

    print("\nKolom akhir:")
    print(feature_data.columns.tolist())

    print("\nPipeline selesai dijalankan.")

if __name__ == "__main__":
    main()