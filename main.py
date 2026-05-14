"""
main.py

Pipeline utama project Stock Recommendation ML v1.0.1.
Untuk tahap ini, main.py baru menjalankan proses data collection.
"""

from src.data_collection import download_stock_data

def main() -> None:
    """
    Fungsi utama untuk menjalankan pipeline project.
    """
    
    ticker = "BBCA.JK"
    star_date = "2018-01-01"
    end_date = None

    data = download_stock_data(
        ticker=ticker,
        start_date=star_date,
        end_date=end_date,
    )

    print(f"\nPreview data:")
    print(data.head())

    print("\nInformasi data:")
    print(data.info())

if __name__ == "__main__":
    main()