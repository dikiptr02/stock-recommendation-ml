from pathlib import Path
import re

# Menentukan lokasi root folder project
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Lokasi file laporan evaluasi berbentuk markdown
EVALUATION_REPORT_PATH = PROJECT_ROOT / "reports" / "evaluation_v1.0.1.md"

def _read_evaluation_report() -> str:
    """
    Membaca isi file reports/evaluation_v1.0.1.md.
    """
    # Mengecek eksistensi file markdown
    if not EVALUATION_REPORT_PATH.exists():
        return ""
    
    # Membaca seluruh teks ke dalam satu string panjang
    return EVALUATION_REPORT_PATH.read_text(encoding="utf-8")

def _extract_metric(text: str, aliases: list[str]) -> float | None:
    """
    Mencari nilai metric berdasarkan beberapa kemungkinana nama metric.

    Contoh format yang bisa terbaca:
    - Accuracy: 0.85
    - accuracy = 0.85
    - | Accuracy | 0.85 |
    - | Precision Macro | 0.82 |
    """
    for alias in aliases:
        # Membuat pola regex (Regular Expression) untuk format teks normal
        normal_patterns  = [
            rf"{alias}\s*[:=]\s*([0-9]*\.?[0-9]+)",  # Format: Metric: 0.85 atau Metric = 0.85
            rf"{alias.replace('_', ' ')}\s*=\s*([0-9]*\.?[0-9]+)",    # Format: Metric = 0.85
            rf"{alias.replace('_', ' ')}\s*[:=]\s*([0-9]*\.?[0-9]+)",  # Format: Metric: 0.85
        ]

        # Membuat pola regex untuk format text di dalam tabel Markdown
        table_patterns = [
            rf"\|\s*{alias}\s*\|\s*([0-9]*\.?[0-9]+)\s*\|",
            rf"\|\s*{alias.replace('_', ' ')}\s*\|\s*([0-9]*\.?[0-9]+)\s*\|",
            rf"\|\s*{alias.replace('_', '-')}\s*\|\s*([0-9]*\.?[0-9]+)\s*\|",
        ]

        # Menggabungkan seluruh skenario pola regex
        patterns = normal_patterns + table_patterns

        # Melakukan pencarian menggunakan semua pola regex tadi
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    # Jika ditemukan, ubah bentuk string angka menjadi Float
                    return float(match.group(1))
                except ValueError:
                    return None
                
    return None

def _extract_confusion_matrix(text: str) -> str | None:
    """
    Mengambil confusion matrix dari laporan evaluasi.

    Bisa membaca format:
    1. Code block Markdown
    2. Tabel markdown setelah heading "Confusion Matrix"
    """
    # Format 1: Mencari confusion matrix yang dibungkus dalam blok kode markdown (```text ... ```)
    code_block_pattern = r"confusion matrix\s*:?\s*```(?:text|python|json)?\s*(.*?)```"
    code_block_match = re.search(
        code_block_pattern, 
        text, 
        re.IGNORECASE | re.DOTALL
        )

    # Jika ketemu di format pertama, langsung return hasilnya
    if code_block_match:
        return code_block_match.group(1).strip()

    # Format 2: Mencari confusion matrix yang di-render murni menggunakan syntax tabel Markdown
    markdown_table_pattern = (
        r"##\s*\d*\.?\s*Confusion Matrix\s*\n\n"
        r"((?:\|.*\|\s*\n?)+)"
    )

    table_match = re.search(
        markdown_table_pattern, 
        text, 
        re.IGNORECASE,
        )

    # Jika ketemu di format kedua, return teks tabelnya
    if table_match:
        return table_match.group(1).strip()
    
    return None

def get_evaluation_summary() -> dict:
    """
    Mengambil ringkasan evaluasi model dari file Markdown.
    Backend v1.1.0 hanya membaca report hasil v1.0.1.
    """
    # Memanggil fungsi pembaca file laporan
    report_text = _read_evaluation_report()

    # Jika file tidak ada, kembalikan respons dengan metric bernilai None
    if not report_text:
        return {
            "report_version": "v1.0.1",
            "source_file": str(EVALUATION_REPORT_PATH),
            "accuracy": None,
            "precision_macro": None,
            "recall_macro": None,
            "f1_macro": None,
            "confusion_matrix": None,
            "raw_report_preview": None,
            "evaluation_status": "Evaluation report file not found",
            "notes": (
                "Pastikan file reports/evaluation_v1.0.1.md tersedia "
                "di folder reports."
            ),
        }
    
    # Ekstrak nilai Accuracy menggunakan bermacam-macam nama alternatif (alias)
    accuracy = _extract_metric(
        report_text, 
        aliases=["accuracy", "akurasi"],
        )
    
    # Ekstrak nilai Precision Macro
    precision_macro = _extract_metric(
        report_text,
        aliases=[
            "precision_macro",
            "precision macro",
            "macro precision",
            "precision macro avg",
        ],
    )

    # Ekstrak nilai Recall Macro
    recall_macro = _extract_metric(
        report_text,
        aliases=[
            "recall_macro",
            "recall macro",
            "macro recall",
            "recall macro avg",
        ]
    )

    # Ekstrak nilai F1-Score Macro
    f1_macro = _extract_metric(
        report_text,
        aliases=[
            "f1_macro",
            "f1 macro",
            "macro f1",
            "f1 macro avg",
        ],
    )

    # Ekstrak bentuk matriks konfusi
    confusion_matrix = _extract_confusion_matrix(report_text)

    # Menyusun format keluaran akhir (dictionary) yang akan dikonsumsi oleh response API
    return {
        "report_version": "v1.0.1",
        "source_file": str(EVALUATION_REPORT_PATH),
        "accuracy": accuracy,
        "precision_macro": precision_macro,
        "recall_macro": recall_macro,
        "f1_macro": f1_macro,
        "confusion_matrix": confusion_matrix,
        "raw_report_preview": report_text[:1000],
        "evaluation_status": "Evaluation report loaded successfully",
        "notes": (
                "Metric dibaca dari reports/evaluation_v1.0.1.md. "
                "Jika ada nilai None, kemungkinan format teks laporan belum "
                "sesuai dengan parser sederhana backend v1.1.0."
        ),
    }