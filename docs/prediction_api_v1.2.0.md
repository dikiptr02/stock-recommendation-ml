# Prediction API Documentation v1.2.0

## Project Name

Stock Recommendation Machine Learning API

## API Version

v1.2.0

## Model Version

v1.0.1

## Description

Prediction API ini digunakan untuk menghasilkan rekomendasi saham berdasarkan fitur teknikal. Output rekomendasi model berupa:

* Buy
* Hold
* Sell

Model yang digunakan pada versi ini adalah model baseline terbaik dari v1.0.1, yaitu Random Forest.

> Disclaimer: API ini dibuat untuk tujuan pembelajaran dan portofolio machine learning. Hasil prediksi tidak boleh dianggap sebagai nasihat investasi.

---

## Base URL

```text
http://127.0.0.1:8000
```

---

## Available Endpoints

| Method | Endpoint             | Description                             |
| ------ | -------------------- | --------------------------------------- |
| GET    | `/`                  | Mengecek status dasar API               |
| GET    | `/health`            | Mengecek health status API              |
| GET    | `/api/v1/model-info` | Menampilkan informasi model             |
| POST   | `/api/v1/predict`    | Menghasilkan prediksi rekomendasi saham |

---

## 1. Root Endpoint

### Request

```http
GET /
```

### Example Response

```json
{
  "message": "Stock Recommendation Prediction API",
  "version": "1.2.0",
  "status": "running"
}
```

---

## 2. Health Check Endpoint

### Request

```http
GET /health
```

### Example Response

```json
{
  "status": "healthy",
  "service": "prediction-api",
  "version": "1.2.0"
}
```

---

## 3. Model Info Endpoint

### Request

```http
GET /api/v1/model-info
```

### Example Response

```json
{
  "status": "success",
  "message": "Model loaded successfully.",
  "data": {
    "is_loaded": true,
    "model_path": "models\\stock_model_v1.0.1.pkl",
    "version": "v1.0.1",
    "model_name": "Random Forest",
    "target_column": "Recommendation",
    "feature_columns": [
      "Daily_Return",
      "MA_5",
      "MA_10",
      "RSI",
      "Volatility",
      "Volume_Change"
    ],
    "classes": [
      "Buy",
      "Hold",
      "Sell"
    ]
  }
}
```

---

## 4. Prediction Endpoint

### Request

```http
POST /api/v1/predict
```

### Request Body

```json
{
  "Daily_Return": 0.012,
  "MA_5": 102.5,
  "MA_10": 101.8,
  "RSI": 55.2,
  "Volatility": 0.03,
  "Volume_Change": 0.12
}
```

---

## Input Fields

| Field           |  Type | Rule         | Description                |
| --------------- | ----: | ------------ | -------------------------- |
| `Daily_Return`  | float | -1.0 to 1.0  | Return harian saham        |
| `MA_5`          | float | > 0          | Moving Average 5 hari      |
| `MA_10`         | float | > 0          | Moving Average 10 hari     |
| `RSI`           | float | 0 to 100     | Relative Strength Index    |
| `Volatility`    | float | 0 to 1.0     | Volatilitas harga saham    |
| `Volume_Change` | float | -1.0 to 10.0 | Perubahan volume transaksi |

---

## Successful Prediction Response

```json
{
  "status": "success",
  "message": "Prediction completed successfully.",
  "prediction": "Buy",
  "confidence": 0.625,
  "probabilities": {
    "Buy": 0.625,
    "Hold": 0.325,
    "Sell": 0.05
  },
  "model_version": "v1.0.1"
}
```

---

## Response Fields

| Field           |   Type | Description                                 |
| --------------- | -----: | ------------------------------------------- |
| `status`        | string | Status response API                         |
| `message`       | string | Pesan hasil request                         |
| `prediction`    | string | Rekomendasi model: Buy, Hold, atau Sell     |
| `confidence`    |  float | Probabilitas tertinggi dari hasil prediksi  |
| `probabilities` | object | Probabilitas untuk setiap class             |
| `model_version` | string | Versi model machine learning yang digunakan |

---

## Invalid Input Example

### Request Body

```json
{
  "Daily_Return": 0.012,
  "MA_5": 102.5,
  "MA_10": 101.8,
  "RSI": 150,
  "Volatility": 0.03,
  "Volume_Change": 0.12
}
```

### Example Error Response

```json
{
  "status": "error",
  "message": "Invalid request input.",
  "errors": [
    {
      "field": "RSI",
      "message": "Input should be less than or equal to 100",
      "value": 150
    }
  ]
}
```

---

## cURL Example

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/predict" ^
-H "Content-Type: application/json" ^
-d "{\"Daily_Return\":0.012,\"MA_5\":102.5,\"MA_10\":101.8,\"RSI\":55.2,\"Volatility\":0.03,\"Volume_Change\":0.12}"
```

---

## Python Request Example

```python
import requests

url = "http://127.0.0.1:8000/api/v1/predict"

payload = {
    "Daily_Return": 0.012,
    "MA_5": 102.5,
    "MA_10": 101.8,
    "RSI": 55.2,
    "Volatility": 0.03,
    "Volume_Change": 0.12,
}

response = requests.post(url, json=payload)

print(response.status_code)
print(response.json())
```

---

## How to Run API

```bash
uvicorn app.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```

---

## Current Model Performance

Based on v1.0.1 evaluation:

| Model               | Accuracy | Macro F1 |
| ------------------- | -------: | -------: |
| Logistic Regression |   0.2972 |   0.2850 |
| Random Forest       |   0.4559 |   0.2982 |

The selected model for this API is Random Forest.

---

## Notes

* This API uses technical indicators as input features.
* The model output is generated from a baseline machine learning model.
* Further model improvement can be added in future versions.
* This API is for educational and portfolio purposes only.
