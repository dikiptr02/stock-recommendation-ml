# Stock Recommendation ML (v1.7.0)

Project ini adalah project pembelajaran Machine Learning *end-to-end* untuk membuat rekomendasi saham harian (Buy, Hold, Sell) berdasarkan data historis harga saham dan indikator teknikal. Saat ini, project telah dilengkapi dengan Backend API Interaktif (FastAPI) yang mampu melayani prediksi saham secara *real-time* maupun dalam jumlah banyak (*batch*), dengan kode yang lebih stabil, terstruktur, dan siap produksi.

> **Catatan Penting:** Project ini ditujukan secara eksklusif untuk pembelajaran dan portofolio data science/machine learning. Output prediksi **bukan** merupakan nasihat investasi finansial.

## Fitur Utama saat ini (v1.7.0)

1. **Prediction by Ticker API**: Memprediksi rekomendasi saham secara instan bermodalkan kode ticker (contoh: `BBCA.JK`). Sistem akan secara otomatis mengunduh data terbaru dan memproses *feature engineering* secara *in-memory*.
2. **Batch Prediction API**: Memproses banyak ticker saham sekaligus secara berurutan dan kebal dari *crash* (*fault-tolerant*) jika ada ticker yang *invalid* atau tidak ditemukan datanya.
3. **Interactive Documentation**: *Swagger UI* bawaan FastAPI terpasang untuk melihat, mengetes, dan membaca deskripsi masing-masing endpoint API.
4. **Project Insights**: Menyediakan *endpoint* laporan untuk melihat akurasi model (*evaluation metric*) dan spesifikasi *Random Forest Classifier* yang menjadi model *baseline*.
5. **Automated Testing**: Project telah dilengkapi dengan unit test dan API test menggunakan Pytest untuk memastikan endpoint, model loader, validation, dan error handling tetap berjalan stabil setelah perubahan kode.

Untuk melihat riwayat lengkap perkembangan fitur dan *bug fix* dari versi awal hingga terkini, silakan baca **[CHANGELOG.md](CHANGELOG.md)**.

## Version v1.7.0 — Refactor Architecture & Routing

Versi ini berfokus pada perapian struktur internal kode. Tidak ada perubahan pada endpoint API, model machine learning, maupun proses training.

### Changes

* Menyatukan dua struktur routing yang terpisah (`app/api/routes/` dan `app/routes/`) menjadi satu struktur konsisten di `app/routes/`.
* Memindahkan `app/api/routes/prediction.py` menjadi `app/routes/prediction_routes.py`.
* Menghapus folder `app/api/` yang sudah tidak digunakan.

### Notes

Versi ini tidak mengubah endpoint URL, model machine learning, file `.pkl`, schemas, services, maupun src pipeline. Fokus update adalah internal code organization dan maintainability.


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

## Menjalankan Automated Test

Jalankan seluruh test:

```bash
python -m pytest
```

Menjalankan test tertentu:

```bash
python -m pytest tests/test_model_loader.py -v
```

Saat versi v1.6.0 dirilis, project memiliki 23 automated tests yang mencakup endpoint API (ticker & batch), validation, error handling, model loader, dan prediction service.


## Daftar Endpoint API

| Method | Endpoint API              | Deskripsi |
| ------ | ------------------------- | --------- |
| GET    | `/`                       | Root endpoint API |
| GET    | `/health`                 | Mengecek status API |
| GET    | `/project-info`           | Menampilkan ringkasan project |
| GET    | `/docs-summary`           | Menampilkan ringkasan dokumentasi |
| GET    | `/model-info`             | Menampilkan metadata model baseline |
| GET    | `/evaluation`             | Menampilkan ringkasan evaluasi model |
| GET    | `/api/v1/model-info`      | Mengecek model loader untuk Prediction API |
| POST   | `/api/v1/predict`         | Prediksi manual berdasarkan fitur teknikal |
| POST   | `/api/v1/predict/ticker`  | Prediksi otomatis berdasarkan ticker |
| POST   | `/api/v1/predict/batch`   | Prediksi beberapa ticker sekaligus |

## Roadmap Selanjutnya
- Menyatukan struktur routing `app/routes/` dan `app/api/routes/` ke satu struktur yang konsisten
- Menyimpan hasil rekomendasi prediksi ke dalam *database*
- Membangun antarmuka (*Frontend Dashboard*) menggunakan React/Vue/Next.js
- Melakukan konfigurasi Auto-Training berkala untuk model ML
- Menerapkan arsitektur *Microservices* dan otentikasi API