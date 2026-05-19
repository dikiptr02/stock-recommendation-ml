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
| Training | 1587 | 2018-01-29 sampai 2024-09-02 |
| Testing | 397 | 2024-09-03 sampai 2026-05-07 |

## 4. Distribusi Label Aktual pada Data Testing

| Recommendation   |   count |
|:-----------------|--------:|
| Hold             |     196 |
| Sell             |     132 |
| Buy              |      69 |

## 5. Distribusi Prediksi Model pada Data Testing

|      |   count |
|:-----|--------:|
| Hold |     323 |
| Buy  |      46 |
| Sell |      28 |

## 6. Evaluation Metrics

| Metric | Score |
|---|---:|
| Accuracy | 0.4509 |
| Precision Macro | 0.3478 |
| Recall Macro | 0.3540 |
| F1 Macro | 0.3133 |
| Precision Weighted | 0.3775 |
| Recall Weighted | 0.4509 |
| F1 Weighted | 0.3720 |

## 7. Classification Report

              precision    recall  f1-score   support

         Buy       0.30      0.20      0.24        69
        Hold       0.49      0.81      0.61       196
        Sell       0.25      0.05      0.09       132

    accuracy                           0.45       397
   macro avg       0.35      0.35      0.31       397
weighted avg       0.38      0.45      0.37       397


## 8. Confusion Matrix

|             |   Predicted Buy |   Predicted Hold |   Predicted Sell |
|:------------|----------------:|-----------------:|-----------------:|
| Actual Buy  |              14 |               48 |                7 |
| Actual Hold |              24 |              158 |               14 |
| Actual Sell |               8 |              117 |                7 |

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
