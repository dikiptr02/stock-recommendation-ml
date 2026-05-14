# Stock Recommendation ML

Project ini adalah project pembelajaran Machine Learning untuk membuat rekomendasi saham berupa:

- Buy
- Hold
- Sell

berdasarkan data historis harga saham, indikator teknikal, dan evaluasi model machine learning.

> Catatan: Project ini hanya untuk pembelajaran dan portofolio data science/machine learning, bukan nasihat invesitasi.

## Version

Current version: v1.0.1

## Tujuan Project

Membangun sistem baseline machine learning yang dapat:

1. Mengambil data historis saham
2. Melakukan prepocessing data
3. Membuat fitur teknikal sederhana
4. Membuat label Buy, Hold, Sell
5. Melatih model machine learning
6. Mengevaluasi model dengan metrik klasifikasi

## Dateset

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

- Daily return
- Moving Average 5 hari
- Moving Average 10 hari
- RSI
- Volatility
- Volume Change

## Model

Model baseline:

- Logistic Regression
- Random Forest Classifier

## Evaluasi

Metrik evaluasi:

- Accuracy
- Precision
- Recall
- F1-Score
- Confusion Matrix

Accuracy saja tidak cukup karena data saham tidak seimbang antara kelas Buy, Hold, dan Sell