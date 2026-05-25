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
