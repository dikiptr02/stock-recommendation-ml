"""
feature_engineering.py

Modul ini digunakan untuk membuat fitur machine learning dari data historis saham yang sudah dibersihkan.

Input:
- data/processes/{ticket}_clean.csv

Output:
- data/processed/{ticker}_features.csv
"""

from pathlib import Path

import numpy as np
import pandas as pd
import logging

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = ["Date", "Open", "High", "Low", "Close", "Volume"]

def calculate_rsi(data: pd.DataFrame, window: int = 14) -> pd.Series:
    """
    Menghitung RSI (Relative Strength Index).
    
    RSI digunakan untuk mengukur momentum perubahan harga.
    Nilai RSI umumnya berada pada rentang 0 sampai 100.
    
    Parameters
    ----------
    data : pd.DataFrame
        Data saham yang memiliki kolom Close.

    window : int
        Periode RSI. Default umum adalah 14 hari.

    Returns
    -------
    pd.Series
        Nilai RSI.

    Notes
    ------
    Implementasi ini menggunakan Simple Moving Average (SMA) untuk menghitung
    avg_gain dan avg_loss - bukan Wilder's Smoothed Moving Average (WSMA)
    yang umum dipakai di platform charting seperti TradingView atau Bloomberg.

    Model v1.0.1 dilatih menggunakan metode SMA ini.
    JANGAN ubah ke WSMA tanpa melakukan training ulang model terlebih dahulu,
    karena akan menghasilkan nilai RSI yang berbeda dari data training.
    """

    delta = data["Close"].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()

    rs = avg_gain / avg_loss
    
    rsi = 100 - (100 / (1 + rs))

    return rsi

def create_features(
        input_path: str = None,
        output_dir: str = "data/processed",
        input_data: pd.DataFrame = None,
        save_file: bool = True,
) -> pd.DataFrame:
    """
    Membuat fitur machine learning dari data saham.
    
    Parameters
    ----------
    input_path : str
        Lokasi file CSV data yang sudah dibersihkan.
        Contoh: "data/processed/BBCA_JK_clean.csv"
        
    output_dir : str
        Folder tujuan untuk menyimpan data yang sudah memiliki fitur.
        
    Returns
    -------
    pd.DataFrame
        DataFrame yang sudah memiliki fitur tambahan.
    """

    if input_data is not None:
        # Data diproses di memory agar endpoint tidak membuat file CSV baru setiap dipanggil
        data = input_data.copy()
        logger.info("Memproses data dari DataFrame memori")
        input_stem = "memory_data"
    else:
        if input_path is None:
            raise ValueError("Harus memberikan input_path atau input_data")
        
        input_file = Path(input_path)
        if not input_file.exists():
            raise FileNotFoundError(f"File tidak ditemukan: {input_path}")
        
        logger.info(f"Membaca data bersih dari: {input_path}")
        data = pd.read_csv(input_file)
        input_stem = input_file.stem

    logger.info(f"Jumlah data sebelum feature engineering: {len(data)} baris")

    # Validasi kolom wajib
    missing_columns = set(REQUIRED_COLUMNS) - set(data.columns)

    if missing_columns:
        raise ValueError(f"Kolom wajib tidak ditemukan: {missing_columns}")
    
    # Pastikan Date bertipe datetime
    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")

    # Urutkan data berdasarkan tanggal
    data = data.sort_values(by="Date").reset_index(drop=True)

    # 1. Daily Return
    data["Daily_Return"] = data["Close"].pct_change()

    # 2. Moving Average 5 hari
    data["MA_5"] = data["Close"].rolling(window=5).mean()

    # 3. Moving Average 10 hari
    data["MA_10"] = data["Close"].rolling(window=10).mean()

    # 4. RSI
    data["RSI"] = calculate_rsi(data, window=14)

    # 5. Volatility
    # Menggunakan rolling standard deviation dari Daily_Return selama 20 hari
    data["Volatility"] = data["Daily_Return"].rolling(window=20).std()

    # 6. Volume Change
    data["Volume_Change"] = data["Volume"].pct_change()

    # Ganti infinity menjadi NaN agar bisa dibersihkan
    data = data.replace([np.inf, -np.inf], np.nan)

    # Hapus baris yang memiliki missing value akibat rolling calculation
    data = data.dropna().reset_index(drop=True)

    logger.info(f"Jumlah data setelah feature engineering: {len(data)} baris")

    if save_file:
        # Buat folder output jika belum ada
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Buat nama file output
        output_filename = input_stem.replace("_clean", "_features") + ".csv"
        output_file = output_path / output_filename

        # Simpan data dengan fitur
        data.to_csv(output_file, index=False)

        logger.info(f"Data fitur berhasil disimpan ke: {output_file}")

    return data

if __name__ == "__main__":
    df = create_features(
        input_path="data/processed/BBCA_JK_clean.csv",
        output_dir="data/processed",
    )

    print("\nPreview data dengan fitur:")
    print(df.head())

    print("\nKolom data:")
    print(df.columns.tolist())