# Changelog

Semua perubahan penting pada project ini akan dicatat di file ini

Format versioning mengikuti Semantic Versioning:

- MAJOR.MINOR.PATCH
- PATCH untuk bug fix/perbaikan kecil
- MINOR untuk penambahan fitur
- MAJOR untuk perubahan besar sistem

Version

- v1.0.1: Baseline machine learning pipeline
- v1.1.0: FastAPI backend documentation
- v1.2.0: Prediction API
- v1.3.0: Prediction by Ticker API
- v1.3.1: Code Cleanup & Refactoring
- v1.4.0: Batch Prediction by Multiple Tickers
- v1.4.1: API Cleanup, Validation, and Consistency
- v1.4.2: Project Cleanup, Documentation Sync, and Minor API Fixes
- v1.5.0: Automated Testing and API Reliability
- v1.6.0: Bug Fixes, Stability & Code Quality
- v1.7.0: Refactor Architecture & Routing


## [v1.7.0] - Refactor Architecture & Routing

### Changed

* Menyatukan dua struktur routing yang terpisah (`app/api/routes/` dan `app/routes/`) menjadi satu struktur konsisten di `app/routes/`.
* Memindahkan dan merename `app/api/routes/prediction.py` menjadi `app/routes/prediction_routes.py`.
* Memperbarui import path di `app/main.py` agar konsisten dengan semua router lainnya.
* Memperbarui mock path di `tests/test_ticker_endpoint.py` dan `tests/test_batch_endpoint.py`.
* Memperbarui import di `tests/test_error_handling.py`.
* Menghapus folder `app/api/` yang sudah tidak digunakan.

### Notes

* Tidak ada perubahan pada endpoint URL — semua route tetap sama.
* Tidak ada perubahan pada model machine learning atau file `.pkl`.
* Tidak ada perubahan pada schemas, services, atau src pipeline.
* Fokus update adalah internal code organization dan maintainability.

## [v1.6.0] - Bug Fixes, Stability & Code Quality

### Fixed

* Memperbaiki typo nama fungsi `_load_pipeline_function` menjadi `_load_pipeline_functions` di `prediction_service.py` — sebelumnya menyebabkan `NameError` saat endpoint `/api/v1/predict/ticker` dan `/api/v1/predict/batch` dipanggil.
* Memperbaiki inkonsistensi key error response pada `GET /api/v1/model-info` dari `"error"` menjadi `"errors"` agar sesuai kontrak API yang distandarkan sejak v1.4.1.
* Memperbaiki pembuatan kolom duplikat `date` di `feature_engineering.py` — konversi datetime kini dilakukan in-place pada kolom `Date`.
* Memperbaiki duplikat entry pada `main_features` di `project_routes.py`.
* Memperbarui `future_development` pada `/docs-summary` agar mencerminkan status project terkini.

### Improved

* Mengganti semua `print()` di `preprocessing.py`, `feature_engineering.py`, dan `data_collection.py` dengan modul `logging` standar Python.
* Menambahkan validator format ticker pada `PredictionTickerRequest` dan `BatchPredictionRequest` agar input tidak valid ditolak lebih awal dengan pesan error yang informatif.
* Menambahkan `startup_event` di `main.py` agar model di-load saat server boot, bukan saat request pertama.
* Menambahkan dokumentasi asumsi implementasi RSI (Simple Moving Average) pada docstring `calculate_rsi()` di `feature_engineering.py`.

### Testing

* Menambahkan `test_ticker_endpoint.py` — test untuk endpoint `/api/v1/predict/ticker` mencakup valid input, format ticker tidak valid, string kosong, dan period tidak valid.
* Menambahkan `test_batch_endpoint.py` — test untuk endpoint `/api/v1/predict/batch` mencakup valid input, partial fail, format ticker tidak valid, list kosong, dan period tidak valid.

## [v1.5.0] - Automated Testing and API Reliability

### Added

* Added automated testing using Pytest.
* Added health endpoint tests.
* Added request validation tests.
* Added prediction API tests.
* Added model loader tests.
* Added error handling tests.
* Added prediction service helper tests.

### Improved

* Added global exception handler for unexpected server errors.
* Standardized JSON error response format across API endpoints.
* Implemented lazy import mechanism for ticker prediction pipeline.
* Improved backend reliability and maintainability.
* Updated project documentation and README.

### Removed

* Removed legacy manual testing scripts from v1.2.0.
* Removed unused root `main.py`.
* Removed empty `scripts/` directory.
* Cleaned obsolete archived testing files.

### Testing

* Total automated tests: 14
* Test status: All tests passing


## [v1.4.2] - 2026-06-08 - Project Cleanup, Documentation Sync, and Minor API Fixes

### Changed

- Update `APP_VERSION` dari `1.4.1` menjadi `1.4.2`.
- Update informasi project dan ringkasan dokumentasi pada endpoint `/project-info` dan `/docs-summary`.
- Update daftar endpoint pada dokumentasi agar sesuai dengan kondisi API terbaru.
- Menyelaraskan README dengan status project v1.4.2.

### Fixed

- Memperbaiki typo kecil pada docstring endpoint model info.
- Merapikan pesan error minor pada endpoint prediksi.
- Menghapus referensi endpoint lama yang sudah tidak relevan dari dokumentasi.

### Removed

- Menghapus folder `__pycache__`.
- Menghapus file cache Python `.pyc` dari project.

### Notes

- Versi ini tidak mengubah model machine learning.
- Versi ini tidak menambahkan endpoint baru.
- Model yang digunakan tetap `models/stock_model_v1.0.1.pkl`.
- Fokus versi ini adalah cleanup patch setelah v1.4.1.

## [v1.4.1] - 2026-06-08 - API Cleanup, Validation, and Consistency

### Added

- Menambahkan `app/core/config.py` untuk menyimpan konfigurasi utama.
- Menambahkan helper function normalisasi ticker di `app/services/prediction_service.py`.

### Changed

- Menggunakan `APP_NAME` dan `APP_VERSION` di `app/main.py`.
- Menggunakan konfigurasi central di seluruh API.

### Fixed

- Menghapus duplicate root endpoint `GET /` di `app/routes/project_routes.py`.
- Memperbaiki validasi `period` yang sebelumnya hanya berupa string menjadi enum `1y`, `5y`, `max`.
- Membatasi batch prediction maksimal 10 ticker.
- Menambahkan normalisasi ticker (strip whitespace, uppercase, deduplicate) pada *prediction service*.
- Memperbaiki potensi bug pada `app/services/model_loader.py` saat membaca class label model.
- Merapikan dan membersihkan logic service.

## [v1.4.0] - 2026-06-05 - Batch Prediction by Multiple Tickers

### Added

- Menambahkan endpoint `POST /api/v1/predict/batch` untuk memprediksi rekomendasi saham dari banyak ticker secara bersamaan.
- Menambahkan schema `BatchPredictionRequest`, `TickerResult`, dan `BatchPredictionResponse`.
- Menambahkan fungsi `predict_batch` pada `prediction_service.py` dengan metode pemrosesan aman (sequential) per ticker.
- Menambahkan dokumen penjelasan `docs/v1.4.0_batch_prediction.md`.

### Changed

- Update semua file *service* di dalam `app/services/` agar memiliki dokumentasi *inline* (komentar baris-per-baris) berbahasa Indonesia.
- Update `README.md` menyesuaikan versi terbaru.

## [v1.3.1] - 2026-06-05 - Code Cleanup & Refactoring

### Removed

- Menghapus 230 baris *dead code* dari `app/services/prediction_service.py`.
- Menghapus *import* ganda `prediction_routes` di `app/main.py`.
- Menghapus file `app/routes/prediction_routes.py` yang sudah *obsolete*.
- Menghapus folder `notebooks/` yang kosong.
- Memindahkan semua testing script lama ke `archive/scripts/v1.2.0/`.

## [v1.3.0] - 2026-06-05 - Prediction by Ticker API

### Added

- Menambahkan endpoint `POST /api/v1/predict/ticker` untuk memprediksi rekomendasi saham.
- Menambahkan class `PredictionTickerRequest` dan `PredictionTickerResponse` di schemas.
- Menambahkan pemrosesan *in-memory* di module data pipeline `src/` agar API berjalan lebih efisien.
- Menambahkan dokumentasi spesifik untuk endpoint baru di `docs/v1.3.0_prediction_by_ticker.md`.

### Changed

- Update parameter opsional (*backward-compatible*) `save_file` dan `input_data` di `src/data_collection.py`, `src/preprocessing.py`, dan `src/feature_engineering.py`.
- Update `README.md` menyesuaikan versi terbaru.

## [v1.2.0] - 2026-xx-xx - Prediction API

### Added

- Menambahkan Prediction API untuk memprediksi rekomendasi saham secara real-time.

## [v1.1.0] - 2026-05-25 - FastAPI Backend Documentation

### Added

- Menambahkan backend sederhana menggunakan FastAPI.
- Menambahkan struktur folder baru `app/`.
- Menambahkan folder `app/routes/` untuk menyimpan endpoint API.
- Menambahkan folder `app/services/` untuk menyimpan logic pembacaan file model, evaluasi, dan prediksi.
- Menambahkan folder `app/schemas/` untuk menyimpan format response API menggunakan Pydantic.
- Menambahkan endpoint `GET /`.
- Menambahkan endpoint `GET /project-info`.
- Menambahkan endpoint `GET /docs-summary`.
- Menambahkan endpoint `GET /model-info`.
- Menambahkan endpoint `GET /evaluation`.
- Menambahkan endpoint `GET /prediction`.
- Menambahkan dokumentasi interaktif backend melalui Swagger UI di `/docs`.
- Menambahkan pembacaan informasi model dari `models/stock_model_v1.0.1.pkl`.
- Menambahkan pembacaan laporan evaluasi dari `reports/evaluation_v1.0.1.md`.
- Menambahkan pembacaan laporan prediksi dari `reports/prediction_v1.0.1.md`.
- Menambahkan pembacaan data processed dari `data/processed/BBCA_JK_labeled.csv`.
- Menambahkan dependency backend `fastapi`.
- Menambahkan dependency server `uvicorn[standard]`.

### Changed

- Project tidak hanya berisi pipeline machine learning, tetapi juga memiliki backend dokumentasi interaktif.
- README diperbarui untuk menjelaskan cara menjalankan backend FastAPI.
- Struktur project dibuat lebih siap untuk dikembangkan menjadi API atau dashboard.
- Dokumentasi project dibuat lebih rapi agar cocok untuk portofolio.

### Fixed

- Menyesuaikan parser backend agar dapat membaca metric evaluasi dari tabel Markdown.
- Menyesuaikan parser backend agar dapat membaca confusion matrix dari tabel Markdown.
- Menyesuaikan parser backend agar hasil prediksi terbaru diprioritaskan dari `prediction_v1.0.1.md`.
- Menyamakan nama field response API dengan schema Pydantic agar tidak terjadi `ResponseValidationError`.

### Notes

- Backend v1.1.0 belum melakukan training ulang model.
- Backend v1.1.0 belum melakukan prediksi real-time dari input user.
- Backend v1.1.0 hanya membaca artefak dari versi v1.0.1.
- Backend ini digunakan sebagai dokumentasi interaktif untuk portofolio machine learning.
- Output model berupa Buy, Hold, atau Sell bukan nasihat investasi.

---

## [v1.0.1] - 2026-05-14 - Baseline Machine Learning Pipeline

### Added

- Membuat pipeline machine learning lengkap.
- Menambahkan tahap data collection.
- Menambahkan tahap preprocessing.
- Menambahkan tahap feature engineering.
- Menambahkan tahap labeling.
- Menambahkan tahap training model.
- Menambahkan tahap evaluation model.
- Menambahkan tahap prediction.
- Melatih model baseline menggunakan Logistic Regression.
- Melatih model baseline menggunakan Random Forest.
- Menyimpan model terbaik ke `models/stock_model_v1.0.1.pkl`.
- Menyimpan laporan evaluasi ke `reports/evaluation_v1.0.1.md`.
- Menyimpan laporan prediksi ke `reports/prediction_v1.0.1.md`.

### Planned

- Data collection dari Yahoo Finance
- Preprocessing data saham
- Feature engineering indikator teknikal
- Labeling Buy, Hold, Sell
- Training Logistic Regression dan Random Forest
- Evaluasi model klasifikasi

### Notes

- Model v1.0.1 masih merupakan baseline awal.
- Project hanya digunakan untuk pembelajaran dan portofolio.
- Hasil prediksi bukan nasihat investasi.
