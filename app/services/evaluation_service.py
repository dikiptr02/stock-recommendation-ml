from pathlib import Path
import re

PROJECT_ROOT = Path(__file__).resolve().parents[2]
EVALUATION_REPORT_PATH = PROJECT_ROOT / "reports" / "evaluation_v1.0.1.md"

def _read_evaluation_report() -> str:
    """
    Membaca isi file reports/evaluation_v1.0.1.md.
    """
    if not EVALUATION_REPORT_PATH.exists():
        return ""
    
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
        normal_patterns  = [
            rf"{alias}\s*[:=]\s*([0-9]*\.?[0-9]+)",  # Format: Metric: 0.85 atau Metric = 0.85
            rf"{alias.replace('_', ' ')}\s*=\s*([0-9]*\.?[0-9]+)",    # Format: Metric = 0.85
            rf"{alias.replace('_', ' ')}\s*[:=]\s*([0-9]*\.?[0-9]+)",  # Format: Metric: 0.85
        ]

        table_patterns = [
            rf"\|\s*{alias}\s*\|\s*([0-9]*\.?[0-9]+)\s*\|",
            rf"\|\s*{alias.replace('_', ' ')}\s*\|\s*([0-9]*\.?[0-9]+)\s*\|",
            rf"\|\s*{alias.replace('_', '-')}\s*\|\s*([0-9]*\.?[0-9]+)\s*\|",
        ]

        patterns = normal_patterns + table_patterns

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
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
    # Format 1: confusion matrix dalam code block
    code_block_pattern = r"confusion matrix\s*:?\s*```(?:text|python|json)?\s*(.*?)```"
    code_block_match = re.search(
        code_block_pattern, 
        text, 
        re.IGNORECASE | re.DOTALL
        )

    if code_block_match:
        return code_block_match.group(1).strip()

    # Format 2: confusion matrix dalam tabel Markdown
    markdown_table_pattern = (
        r"##\s*\d*\.?\s*Confusion Matrix\s*\n\n"
        r"((?:\|.*\|\s*\n?)+)"
    )

    table_match = re.search(
        markdown_table_pattern, 
        text, 
        re.IGNORECASE,
        )

    if table_match:
        return table_match.group(1).strip()
    
    return None

def get_evaluation_summary() -> dict:
    """
    Mengambil ringkasan evaluasi model dari file Markdown.
    Backend v1.1.0 hanya membaca report hasil v1.0.1.
    """
    report_text = _read_evaluation_report()

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
    
    accuracy = _extract_metric(
        report_text, 
        aliases=["accuracy", "akurasi"],
        )
    
    precision_macro = _extract_metric(
        report_text,
        aliases=[
            "precision_macro",
            "precision macro",
            "macro precision",
            "precision macro avg",
        ],
    )

    recall_macro = _extract_metric(
        report_text,
        aliases=[
            "recall_macro",
            "recall macro",
            "macro recall",
            "recall macro avg",
        ]
    )

    f1_macro = _extract_metric(
        report_text,
        aliases=[
            "f1_macro",
            "f1 macro",
            "macro f1",
            "f1 macro avg",
        ],
    )

    confusion_matrix = _extract_confusion_matrix(report_text)

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