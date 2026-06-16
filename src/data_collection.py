"""
data_collection.py

Modul ini digunakan untuk mengambil data historis saham dari Yahoo Finance
menggunakan library yfinance.

Output:
- File CSV berisi data historis saham di folder data/raw/
"""

from pathlib import Path
from typing import Optional

import pandas as pd
import yfinance as yf

REQUIRED_COLUMNS = ["Date", "Open", "High", "Low", "Close", "Volume"]

def download_stock_data(
        ticker: str,
        start_date: str,
        end_date: Optional[str] = None,
        output_dir: str = "data/raw",
        save_file: bool = True,
    ) -> pd.DataFrame:
    """
    Mengambil data historis saham dari Yahoo Finance.

    Paremeter
    ----------
    ticker : str
        Kode ticker saham.
        Contoh:
        - BBCA.JK untuk Bank Central Asia Tbk.
        - BBRI.JK untuk Bank Rakyat Indonesia Tbk.
        - AAPL untuk Apple Inc.
        - MSFT untuk Microsoft Corporation.

    start_date : str
        Tanggal mulai data, format YYYY-MM-DD.
        Contoh: "2018-01-01"
    
    end_date : Optional[str]
        Tanggal akhir data, format YYYY-MM-DD.
        Jika None, yfinance akan mengambil data sampai terbaru yang tersedia.

    output_dir : str
        Folder tujuan untuk menyimpan file CSV.
    
    Returns
    -------
    pd.DataFrame
        DataFrame berisi data historis saham.
    """

    logger.info(f"Mengambil data saham: {ticker}")
    logger.info(f"Periode mulai: {start_date}")
    logger.info(f"Periode akhir: {end_date if end_date else 'data terbaru'}")

    data = yf.download(
        tickers=ticker,
        start=start_date,
        end=end_date,
        interval="1d",
        auto_adjust=False,
        progress=False,
    )

    if data.empty:
        raise ValueError(
            f"Data untuk ticker {ticker} kosong."
            "Periksa kembali kode ticker atau koneksi internet."
        )
    
    # Jika yfinance menghasilkan Multiindex column, ubah menjadi single-level column.
    # Ini berguna agar kolom menjadi  Open, High, Low, Close, Volume.
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    # Ubah index Data menjadi kolom biasa
    data = data.reset_index()

    # Ambil hanya kolom utama yang dibutuhkan
    available_columns = [col for col in REQUIRED_COLUMNS if col in data.columns]
    data = data[available_columns]

    # Validasi kolom wajib
    missing_columns = set(REQUIRED_COLUMNS) - set(data.columns)
    if missing_columns:
        raise ValueError(f"Kolom berikut tidak ditemukan: {missing_columns}")
    
    if save_file:
        # Buat folder output jika belum ada
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Nama file output
        clean_ticker_name = ticker.replace(".", "_")
        file_path = output_path / f"{clean_ticker_name}_raw.csv"

        # Simpan ke CSV
        data.to_csv(file_path, index=False)

        logger.info(f"Data berhasil disimpan ke: {file_path}")
        
    logger.info(f"Jumlah baris data: {len(data)}")

    return data

if __name__ == "__main__":
    # Contoh menjalankan langsung file ini
    df = download_stock_data(
        ticker="BBCA.JK",
        start_date="2018-01-01",
        end_date=None,
    )

    print(df.head())