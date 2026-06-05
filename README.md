# Stock Recommendation ML

Project ini adalah project pembelajaran Machine Learning untuk membuat rekomendasi saham berupa:

- Buy
- Hold
- Sell

berdasarkan data historis harga saham, indikator teknikal, dan evaluasi model machine learning.

> Catatan: Project ini hanya untuk pembelajaran dan portofolio data science/machine learning, bukan nasihat investasi.

## Version

Current version: v1.3.0

### Version History

| Version | Fokus Pengembangan                                                   |
| ------- | -------------------------------------------------------------------- |
| v1.0.1  | Pipeline machine learning baseline untuk rekomendasi Buy, Hold, Sell |
| v1.1.0  | Backend dokumentasi interaktif menggunakan FastAPI                   |
| v1.2.0  | Prediction API untuk prediksi real-time menggunakan input user       |
| v1.3.0  | Prediction API berdasarkan Ticker saham (Prediction by Ticker)       |

## Tujuan Project

Membangun sistem baseline machine learning yang dapat:

1. Mengambil data historis saham
2. Melakukan preprocessing data
3. Membuat fitur teknikal sederhana
4. Membuat label Buy, Hold, Sell
5. Melatih model machine learning
6. Mengevaluasi model dengan metrik klasifikasi
7. Menampilkan informasi project, model, evaluasi, dan prediksi melalui backend FastAPI

## Dataset

Minimal kolom yang digunakan:

- Date
- Open
- High
- Low
- Close
- Volume

Sumber data dapat berasal dari:

- Yahoo Finance melalui yfinance
- CSV manual
- Sumber data saham lain

## Fitur Machine Learning v1.0.1

Fitur yang digunakan:

- Daily Return
- Moving Average 5 hari
- Moving Average 10 hari
- RSI
- Volatility
- Volume Change

## Model

Model baseline:

- Logistic Regression
- Random Forest Classifier

Model terbaik yang digunakan pada versi v1.0.1:

- Random Forest

Model disimpan pada:

```text
models/stock_model_v1.0.1.pkl
```

## Evaluasi

Metrik evaluasi:

- Accuracy
- Precision
- Recall
- F1-Score
- Confusion Matrix

Accuracy saja tidak cukup karena data saham tidak seimbang antara kelas Buy, Hold, dan Sell.

Laporan evaluasi disimpan pada:

```text
reports/evaluation_v1.0.1.md
```

## Prediction Report

Hasil prediksi terbaru disimpan pada:

```text
reports/prediction_v1.0.1.md
```

Output prediksi berupa:

- Buy
- Hold
- Sell

---

# Version v1.1.0 - FastAPI Backend Documentation

Pada versi v1.1.0, project menambahkan backend sederhana menggunakan **FastAPI**.

Backend ini digunakan sebagai dokumentasi interaktif untuk menampilkan informasi:

- Project
- Model machine learning
- Evaluasi model
- Hasil prediksi terbaru
- Ringkasan dokumentasi project

Backend v1.1.0 **tidak melakukan training ulang** dan **belum melakukan prediksi real-time**. Backend hanya membaca artefak hasil pipeline dari versi v1.0.1.

## Tujuan v1.1.0

Tujuan utama versi v1.1.0 adalah merapikan sistem dokumentasi project dengan menambahkan backend sederhana agar hasil pipeline machine learning dapat diakses melalui endpoint API.

Backend ini juga menjadi pondasi awal jika project ingin dikembangkan menjadi:

- API prediksi real-time
- Dashboard machine learning
- Sistem monitoring model
- Backend portfolio project

## File yang Dibaca Backend

Backend v1.1.0 membaca file hasil dari versi v1.0.1 berikut:

```text
models/stock_model_v1.0.1.pkl
reports/evaluation_v1.0.1.md
reports/prediction_v1.0.1.md
data/processed/BBCA_JK_labeled.csv
data/processed/BBCA_JK_features.csv
```

## Struktur Backend v1.1.0

```text
app/
├── __init__.py
├── main.py
│
├── routes/
│   ├── __init__.py
│   ├── project_routes.py
│   ├── model_routes.py
│   ├── evaluation_routes.py
│   └── prediction_routes.py
│
├── services/
│   ├── __init__.py
│   ├── model_service.py
│   ├── evaluation_service.py
│   └── prediction_service.py
│
└── schemas/
    ├── __init__.py
    ├── model_schema.py
    ├── evaluation_schema.py
    └── prediction_schema.py
```

## Penjelasan Folder Backend

| Folder          | Fungsi                                                |
| --------------- | ----------------------------------------------------- |
| `app/main.py`   | File utama aplikasi FastAPI                           |
| `app/routes/`   | Menyimpan endpoint API                                |
| `app/services/` | Menyimpan logic untuk membaca model, report, dan data |
| `app/schemas/`  | Menyimpan format response API menggunakan Pydantic    |

## Endpoint Backend

| Method | Endpoint        | Deskripsi                                        |
| ------ | --------------- | ------------------------------------------------ |
| GET    | `/`             | Menampilkan informasi singkat project            |
| GET    | `/project-info` | Menampilkan tujuan, deskripsi, dan fitur project |
| GET    | `/docs-summary` | Menampilkan ringkasan dokumentasi project        |
| GET    | `/model-info`   | Menampilkan informasi model terbaik              |
| GET    | `/evaluation`   | Menampilkan ringkasan evaluasi model             |
| GET    | `/prediction`   | Menampilkan hasil prediksi terbaru               |

## Cara Menjalankan Backend di Local

Pastikan terminal berada di root project:

```text
stock-recommendation-ml v1.0.1/
```

Aktifkan virtual environment:

```bash
.venv\Scripts\activate
```

Install dependency:

```bash
python -m pip install -r requirements.txt
```

Jalankan server FastAPI:

```bash
python -m uvicorn app.main:app --reload
```

Jika ingin memastikan menggunakan Python dari virtual environment, gunakan:

```bash
.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Jika berhasil, backend akan berjalan di:

```text
http://127.0.0.1:8000
```

## Cara Test Endpoint Melalui Browser

Buka endpoint berikut di browser:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/project-info
http://127.0.0.1:8000/docs-summary
http://127.0.0.1:8000/model-info
http://127.0.0.1:8000/evaluation
http://127.0.0.1:8000/prediction
```

## Cara Test Melalui Swagger UI

FastAPI menyediakan dokumentasi API interaktif melalui Swagger UI.

Buka:

```text
http://127.0.0.1:8000/docs
```

Langkah test endpoint:

1. Pilih endpoint yang ingin diuji.
2. Klik **Try it out**.
3. Klik **Execute**.
4. Pastikan response code adalah `200`.

## Contoh Output Endpoint `/model-info`

```json
{
  "model_version": "v1.0.1",
  "best_model_name": "Random Forest",
  "model_type": "Pipeline",
  "total_features": 6,
  "features_used": [
    "Daily_Return",
    "MA_5",
    "MA_10",
    "RSI",
    "Volatility",
    "Volume_Change"
  ],
  "target_prediction": "Recommendation",
  "model_status": "Model loaded successfully"
}
```

## Contoh Output Endpoint `/evaluation`

```json
{
  "report_version": "v1.0.1",
  "accuracy": 0.4559,
  "precision_macro": 0.3367,
  "recall_macro": 0.3462,
  "f1_macro": 0.2982,
  "evaluation_status": "Evaluation report loaded successfully"
}
```

## Contoh Output Endpoint `/prediction`

```json
{
  "model_version": "v1.0.1",
  "latest_data_date": "2026-05-19",
  "latest_close_price": 5950.0,
  "recommendation": "Hold",
  "probabilities": {
    "Buy": 0.31,
    "Hold": 0.395,
    "Sell": 0.295
  },
  "prediction_status": "Prediction report loaded successfully"
}
```

## Requirements Tambahan v1.1.0

Untuk menjalankan backend, dependency utama yang dibutuhkan adalah:

```text
fastapi
uvicorn[standard]
```

Dependency tersebut sudah ditambahkan ke:

```text
requirements.txt
```

## Catatan Penting

Project ini hanya digunakan untuk pembelajaran dan portofolio machine learning.

Output model berupa rekomendasi:

```text
Buy
Hold
Sell
```

bukan merupakan nasihat investasi.

Model v1.0.1 masih merupakan baseline awal, sehingga hasil prediksi harus dipahami sebagai eksperimen machine learning.

## Keterbatasan Backend v1.1.0

Backend v1.1.0 masih memiliki beberapa keterbatasan:

- Belum melakukan training ulang model
- Belum melakukan prediksi real-time dari input user
- Belum mendukung banyak kode saham
- Belum menggunakan database
- Belum memiliki frontend dashboard
- Belum memiliki autentikasi API
- Belum dideploy ke server/cloud

---

# Version v1.2.0 - Prediction API

Pada versi v1.2.0, project menambahkan endpoint Prediction API yang dapat menerima input fitur teknikal dari user dan menghasilkan rekomendasi saham secara langsung.

Endpoint utama pada versi ini adalah:

```text
POST /api/v1/predict

## Roadmap Versi Berikutnya

Rencana pengembangan berikutnya:

- Menambahkan dukungan multi saham
- Menambahkan fitur auto feature engineering dari data harga terbaru
- Menyimpan hasil prediksi ke database
- Membuat dashboard frontend
- Menambahkan autentikasi API
- Deploy backend ke cloud
- Meningkatkan performa model pada versi berikutnya

---

# Version v1.3.0 - Prediction by Ticker API

Pada versi v1.3.0, project menambahkan fitur untuk memprediksi rekomendasi saham secara instan dengan bermodalkan input **kode ticker**. Sistem secara dinamis akan mengambil data historis saham, menghitung fitur teknikal di memori, dan mengembalikan rekomendasi Buy/Hold/Sell.

Endpoint utama pada versi ini adalah:

```text
POST /api/v1/predict/ticker
```

Untuk detail dokumentasi lengkap mengenai API terbaru, payload request/response, beserta catatan penggunaannya, silakan mengacu ke dokumen berikut:
[Dokumentasi API v1.3.0: Prediction by Ticker](docs/v1.3.0_prediction_by_ticker.md)
