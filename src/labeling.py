"""
labeling.py

Modul ini digunakan untuk membuat label rekomendasi saham:
Buy, Hold, atau Sell.

Input:
- data/processed/{ticket}_features.csv

Output:
- data/processed/{ticker}_labeled.csv
"""

from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = ["Date", "Open", "High", "Low", "Close", "Volume", "Daily_Return", "MA_5", "MA_10", "RSI", "Volatility", "Volume_Change"]

def create_recommendation_label(
    future_return: float,
    buy_threshold: float, 
    sell_threhold: float,
) -> str:
    """
    Membuat label rekomendasi berdasarkan future return.
    
    Parameters
    ----------
    future_return : float
        Return harga saham beberapa hari ke depan.
        
    buy_threshold : float
        Batas minimal return agar diberi label Buy.
    
    sell_threshold : float
        Batas maksimal return negatif agar diberi label Sell.

    Returns
    -------
    str
        Label rekomendasi: "Buy", "Hold", atau "Sell".
    """

    if future_return > buy_threshold:
        return "Buy"
    
    if future_return < sell_threhold:
        return "Sell"
    
    return "Hold"

def create_labels(
    input_path: str,
    output_dir: str = "data/processed",
    horizon: int = 5,
    buy_threshold: float = 0.02,
    sell_threshold: float = -0.02,
) -> pd.DataFrame:
    """
    Membuat label Buy, Hold, Sell berdasarkan return masa depan.
    
    Parameters
    ----------
    input_path : str
        Lokasi file CSV yang sudah memiliki fitur.
        Contoh: "data/processed/BBCA_JK_features.csv
    
    output_dir : str
        Folder tujuan untuk menyimpan data yang sudah memiliki label.
    
    horizon : int
        Jarak hari ke depan untuk menghitung future return.
        Default 5 hari.
        
    buy_threshold : float
        Threshold positif untuk label Buy.
        Default 0.02 atau 2%.
        
    sell_threshold : float
        Threshold negatif untuk label Sell.
        Default -0.02 atau -2%.

    Returns
    -------
    pd.DataFrame
        DataFrame yang sudah memiliki kolom Future_Return dan Recommendation.
    """

    input_file = Path(input_path)

    if not input_file.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {input_file}")
    
    print(f"Membaca data fitur dari: {input_path}")

    data = pd.read_csv(input_file)

    print(f"Jumlah data sebelum labeling: {len(data)}")

    # Validasi kolom wajib
    missing_columns = set(REQUIRED_COLUMNS) - set(data.columns)

    if missing_columns:
        raise ValueError(f"Kolom wajib tidak ditemukan: {missing_columns}")
    
    # Pastikan Date bertipe datetime dan data urut berdasarkan waktu
    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
    data = data.sort_values("Date").reset_index(drop=True)

    # Menghitung harga Close beberapa hari ke depan
    data["Future_Close"] = data["Close"].shift(-horizon)

    # Menghitung future return
    data["Future_Return"] = data["Future_Close"] / data["Close"] - 1

    # Membuat label Buy, Hold, Sell
    data["Recommendation"] = data["Future_Return"].apply(
        lambda x: create_recommendation_label(
            future_return=x,
            buy_threshold=buy_threshold,
            sell_threhold=sell_threshold,
        )
    )

    # Hapus baris terakhir yang tidak punya Future_Close
    # Karena data beberapa hari ke depan belum tersedia
    data = data.dropna(subset=["Future_Close", "Future_Return"]).reset_index(drop=True)

    # Hapus kolom Future_Close agar tidak dipakai sebagai fitur model
    data = data.drop(columns=["Future_Close"])

    print(f"Jumlah data setelah labeling: {len(data)} baris")

    print("\nDistribusi label:")
    print(data["Recommendation"].value_counts())

    print("\nDistribusi label dalam persen:")
    print(data["Recommendation"].value_counts(normalize=True) * 100)

    # Buat folder output jika belum ada
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Buat nama file output
    output_filename = input_file.stem.replace("_features", "_labeled") + ".csv"
    output_file = output_path / output_filename

    # Simpan data berlabel
    data.to_csv(output_file, index=False)

    print(f"\nData berlabel berhasil disimpan ke: {output_file}")

    return data

if __name__ == "__main__":
    df = create_labels(
        input_path="data/processed/BBCA_JK_features.csv",
        output_dir="data/processed",
        horizon=5,
        buy_threshold=0.02,
        sell_threshold=-0.02,
    )

    print("\nPreview data berlabel:")
    print(df.head())

    print("\nKolom data:")
    print(df.columns.tolist())