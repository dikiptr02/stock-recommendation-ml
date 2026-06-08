# Stock Recommendation ML (v1.4.1)

Project ini adalah project pembelajaran Machine Learning *end-to-end* untuk membuat rekomendasi saham harian (Buy, Hold, Sell) berdasarkan data historis harga saham dan indikator teknikal. Saat ini, project telah dilengkapi dengan Backend API Interaktif (FastAPI) yang mampu melayani prediksi saham secara *real-time* maupun dalam jumlah banyak (*batch*).

> **Catatan Penting:** Project ini ditujukan secara eksklusif untuk pembelajaran dan portofolio data science/machine learning. Output prediksi **bukan** merupakan nasihat investasi finansial.

## Fitur Utama saat ini (v1.4.0)

1. **Prediction by Ticker API**: Memprediksi rekomendasi saham secara instan bermodalkan kode ticker (contoh: `BBCA.JK`). Sistem akan secara otomatis mengunduh data terbaru dan memproses *feature engineering* secara *in-memory*.
2. **Batch Prediction API**: Memproses banyak ticker saham sekaligus secara berurutan dan kebal dari *crash* (*fault-tolerant*) jika ada ticker yang *invalid* atau tidak ditemukan datanya.
3. **Interactive Documentation**: *Swagger UI* bawaan FastAPI terpasang untuk melihat, mengetes, dan membaca deskripsi masing-masing endpoint API.
4. **Project Insights**: Menyediakan *endpoint* laporan untuk melihat akurasi model (*evaluation metric*) dan spesifikasi *Random Forest Classifier* yang menjadi model *baseline*.

Untuk melihat riwayat lengkap perkembangan fitur dan *bug fix* dari versi awal hingga terkini, silakan baca **[CHANGELOG.md](CHANGELOG.md)**.

## Version v1.4.1 — API Cleanup, Validation, and Consistency

Versi **v1.4.1** merupakan patch release setelah v1.4.0. Fokus utama versi ini adalah membersihkan struktur API, memperkuat validasi request, dan membuat metadata versi project lebih konsisten.

### Main Improvements

* Menambahkan central configuration melalui `app/core/config.py`.
* Menggunakan `APP_NAME` dan `APP_VERSION` secara konsisten di `app/main.py`.
* Menghapus duplicate root endpoint agar `GET /` hanya dikelola dari `app/main.py`.
* Memperkuat validasi request untuk single ticker prediction dan batch prediction.
* Membatasi input batch prediction maksimal 10 ticker.
* Membatasi nilai `period` hanya pada pilihan valid: `1y`, `5y`, dan `max`.
* Menambahkan normalisasi ticker:

  * menghapus spasi di awal/akhir input,
  * mengubah ticker menjadi uppercase,
  * menghapus ticker duplikat pada batch prediction.
* Memperbaiki potensi bug pada `model_loader.py` saat membaca class label model.
* Membersihkan dan merapikan logic di `prediction_service.py`.

### Validation Rules

Single ticker prediction:

```json
{
  "ticker": "BBCA.JK",
  "period": "5y"
}
```

Batch prediction:

```json
{
  "tickers": ["BBCA.JK", "TLKM.JK"],
  "period": "5y"
}
```

Valid `period` values:

```text
1y
5y
max
```

Maximum batch tickers:

```text
10 tickers per request
```

### Notes

Versi ini tidak mengubah model machine learning, file `.pkl`, logic training, maupun label rekomendasi. Perubahan hanya berfokus pada API cleanup, request validation, dan konsistensi struktur kode.

## Dokumentasi Modul Spesifik

Untuk mengetahui detail cara penggunaan spesifik *endpoint* beserta contoh bentuk *payload JSON*-nya, pelajari dokumen ini:
- [Dokumentasi API v1.3.0: Prediction by Ticker](docs/v1.3.0_prediction_by_ticker.md)
- [Dokumentasi API v1.4.0: Batch Prediction](docs/v1.4.0_batch_prediction.md)

## Struktur Folder Inti

```text
app/
├── main.py                # File utama (entry point) aplikasi FastAPI
├── routes/                # Kumpulan Endpoint API (Controller)
├── services/              # Logika pengolahan prediksi, pembacaan model, & evaluasi
└── schemas/               # Skema input-output request Pydantic

src/                       # Pipeline proses Machine Learning murni
docs/                      # Kumpulan dokumentasi panduan fitur
models/                    # Tempat penyimpanan fisik model ML (.pkl)
reports/                   # Rekaman laporan model (evaluasi & log prediksi manual)
archive/                   # Tempat penyusutan file atau script testing usang
```

## Cara Menjalankan Backend API

1. Pastikan terminal berada di lokasi folder root proyek.
2. Aktifkan *Virtual Environment*:
   ```bash
   .venv\Scripts\activate
   ```
3. *Install dependencies* yang dibutuhkan:
   ```bash
   python -m pip install -r requirements.txt
   ```
4. Nyalakan server web Uvicorn:
   ```bash
   python -m uvicorn app.main:app --reload
   ```
5. Buka Swagger UI interaktif di *browser* Anda:
   ```text
   http://127.0.0.1:8000/docs
   ```

## Daftar Endpoint API

| Method | Endpoint API                    | Deskripsi Fungsionalitas                               |
| ------ | ------------------------------- | ------------------------------------------------------ |
| GET    | `/project-info`                 | Menampilkan ringkasan dan metadata project             |
| GET    | `/model-info`                   | Menampilkan metadata model baseline (Random Forest)    |
| GET    | `/evaluation`                   | Menampilkan performa (Accuracy, Precision, dll)        |
| POST   | `/api/v1/predict`               | Prediksi saham menggunakan input fitur teknikal manual |
| POST   | `/api/v1/predict/ticker`        | Prediksi otomatis berdasarkan satu kode ticker         |
| POST   | `/api/v1/predict/batch`         | Prediksi multi-saham (array) menggunakan list ticker   |

## Roadmap Selanjutnya
- Melakukan konfigurasi Auto-Training berkala untuk model ML
- Menyimpan hasil rekomendasi prediksi ke dalam *database*
- Membangun antarmuka (*Frontend Dashboard*) menggunakan React/Vue/Next.js
- Menerapkan arsitektur *Microservices* dan otentikasi API
