# Evaluation Report - Stock Recommendation ML v1.0.1

## 1. Ringkasan Model

| Item | Keterangan |
|---|---|
| Version | v1.0.1 |
| Model terbaik | Random Forest |
| Target | Recommendation |
| Jumlah fitur | 6 |

## 2. Fitur yang Digunakan

- Daily_Return
- MA_5
- MA_10
- RSI
- Volatility
- Volume_Change

## 3. Pembagian Data

Data dibagi menggunakan **time-based split**, yaitu data lama sebagai training dan data terbaru sebagai testing.

| Dataset | Jumlah Data | Periode |
|---|---:|---|
| Training | 1588 | 2018-01-29 sampai 2024-09-03 |
| Testing | 397 | 2024-09-04 sampai 2026-05-08 |

## 4. Distribusi Label Aktual pada Data Testing

| Recommendation   |   count |
|:-----------------|--------:|
| Hold             |     195 |
| Sell             |     133 |
| Buy              |      69 |

## 5. Distribusi Prediksi Model pada Data Testing

|      |   count |
|:-----|--------:|
| Hold |     330 |
| Buy  |      41 |
| Sell |      26 |

## 6. Evaluation Metrics

| Metric | Score |
|---|---:|
| Accuracy | 0.4559 |
| Precision Macro | 0.3367 |
| Recall Macro | 0.3462 |
| F1 Macro | 0.2982 |
| Precision Weighted | 0.3767 |
| Recall Weighted | 0.4559 |
| F1 Weighted | 0.3680 |

## 7. Classification Report

              precision    recall  f1-score   support

         Buy       0.24      0.14      0.18        69
        Hold       0.50      0.84      0.62       195
        Sell       0.27      0.05      0.09       133

    accuracy                           0.46       397
   macro avg       0.34      0.35      0.30       397
weighted avg       0.38      0.46      0.37       397


## 8. Confusion Matrix

|             |   Predicted Buy |   Predicted Hold |   Predicted Sell |
|:------------|----------------:|-----------------:|-----------------:|
| Actual Buy  |              10 |               52 |                7 |
| Actual Hold |              19 |              164 |               12 |
| Actual Sell |              12 |              114 |                7 |

## 9. Interpretasi Singkat

Model ini adalah baseline awal untuk project pembelajaran dan portofolio.

Catatan penting:

- Accuracy tidak cukup untuk menilai model.
- Macro F1-score penting karena kelas Buy, Hold, dan Sell bisa tidak seimbang.
- Confusion matrix digunakan untuk melihat kesalahan prediksi tiap kelas.
- Model ini belum boleh digunakan sebagai nasihat investasi nyata.

## 10. Keterbatasan Model v1.0.1

- Fitur masih sederhana.
- Belum ada hyperparameter tuning.
- Belum ada walk-forward validation.
- Belum ada backtesting.
- Belum memperhitungkan biaya transaksi.
- Belum menggunakan data fundamental.
- Belum menggunakan data sentimen berita.

## 11. Disclaimer

Project ini hanya untuk pembelajaran dan portofolio data science/machine learning.

Output model bukan nasihat investasi.
