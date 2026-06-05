"""
preprocessing.py

Modul ini digunakan untuk membersihkan data historis saham
agar siap digunakan untuk feature engineering dan machine learning.

Input:
- data/raw/{ticker}_raw.csv

Output:
- data/processed/{ticker}_clean.csv
"""

from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = ["Date", "Open", "High", "Low", "Close", "Volume"]

def preprocess_stock_data(
    input_path: str = None,
    output_dir: str = "data/processed",
    input_data: pd.DataFrame = None,
    save_file: bool = True,
) -> pd.DataFrame:
    """
    Membersihkan data historis saham.

    Parameters
    ----------
    input_path : str
        Lokasi file CSV data mentah.
        Contoh: "data/raw/BBCA_JK_raw.csv"

    output_dir : str
        Folder tujuan untuk menyimpan data yang sudah dibersihkan.

    Returns
    -------
    pd.DataFrame
        DataFrame sudah dibersihkan.
    """

    if input_data is not None:
        # Data diproses di memory agar endpoint tidak membuat file CSV baru setiap dipanggil
        data = input_data.copy()
        print("Memproses data dari DataFrame memori")
        input_stem = "memory_data"
    else:
        if input_path is None:
            raise ValueError("Harus memberikan input_path atau input_data")
        
        input_file = Path(input_path)
        if not input_file.exists():
            raise FileNotFoundError(f"File tidak ditemukan: {input_path}")
        
        print(f"Membaca data dari: {input_path}")
        data = pd.read_csv(input_file)
        input_stem = input_file.stem

    print(f"Jumlah data awal: {len(data)} baris")

    # Validasi kolom wajib
    missing_columns = set(REQUIRED_COLUMNS) - set(data.columns)

    if missing_columns:
        raise ValueError(f"Kolom wajib tidak ditemukan: {missing_columns}")
    
    # Ambil hanya kolom yang dibutuhkan
    data = data[REQUIRED_COLUMNS].copy()

    # Ubah kolom Data menjadi datetime
    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")

    # Ubah kolom numerik
    numeric_columns = ["Open", "High", "Low", "Close", "Volume"]

    for column in numeric_columns:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    # Hapus duplikat penuh
    data = data.drop_duplicates()

    # Hapus duplikat berdasarkan tanggal
    # Jika ada tanggal yang sama, ambil data terakhir
    data = data.drop_duplicates(subset=["Date"], keep="last")

    # Hapus missing value
    data = data.dropna(subset=REQUIRED_COLUMNS)

    # Urutkan berdasarkan tanggal
    data = data.sort_values(by="Date").reset_index(drop=True)

    print(f"Jumlah data setelah dibersihkan: {len(data)} baris")

    if save_file:
        # Buat folder output jika belum ada
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Buat nama file output
        output_filename = input_stem.replace("_raw", "_clean") + ".csv"
        output_file = output_path / output_filename

        # Simpan data bersih
        data.to_csv(output_file, index=False)

        print(f"Data bersih berhasil disimpan ke: {output_file}")

    return data

if __name__ == "__main__":
    df = preprocess_stock_data(
        input_path="data/raw/BBCA_JK_raw.csv",
        output_dir="data/processed",
    )

    print(f"\nPreview data bersih:")
    print(df.head())

    print("\nInformasi data bersih:")
    print(df.info())