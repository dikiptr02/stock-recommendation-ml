from pathlib import Path
import sys

# Tambahkan root project ke Python path
ROOT_DIR = Path(__file__).resolve().parents[1]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.services.model_loader import model_loader

def main():
    print("=== Manual Test Model Loader v1.2.0 ===")

    model_loader.load_model()

    info = model_loader.get_model_info()

    print("\nModel Info:")
    for key, value in info.items():
        print(f"{key}: {value}")

    sample_input = {
        "Daily_Return": 0.012,
        "MA_5": 102.5,
        "MA_10": 101.8,
        "RSI": 55.2,
        "Volatility": 0.03,
        "Volume_Change": 0.12,
    }

    result = model_loader.predict(sample_input)

    print("\nPrediction Result:")
    print(result)

    print("\nManual test model loader selesai.")

if __name__ == "__main__":
    main()