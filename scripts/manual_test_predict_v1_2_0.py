from pathlib import Path
import joblib
import pandas as pd

MODEL_PATH = Path("models/stock_model_v1.0.1.pkl")

def inspect_dict_model(model_bundle):
    """
    Menampilkan isi utama dari file model jika ternyata berupa dictionary.
    """
    print("\nModel file berisi dictionary dengan key berikut:")

    for key, value in model_bundle.items():
        print(f"- {key}: {type(value)}")

def find_model_from_dict(model_bundle):
    """
    Mencari object model sklearn di dalam dictionary.
    Model sklearn biasanya punya method predict().
    """
    possible_model_keys = [
        "model",
        "best_model",
        "trained_model",
        "classifier",
        "clf",
        "pipeline",
    ]

    for key in possible_model_keys:
        if key in model_bundle and hasattr(model_bundle[key], "predict"):
            print(f"\nModel ditemukan pada key: '{key}'")
            return model_bundle[key]

    for key, value in model_bundle.items():
        if hasattr(value, "predict"):
            print(f"\nModel ditemukan pada key: '{key}'")
            return value

    return None

def find_features_from_dict(model_bundle):
    """
    Mencari daftar fitur di dalam dictionary.
    """
    possible_feature_keys = [
        "features",
        "feature_names",
        "feature_columns",
        "columns",
        "selected_features",
        "input_features",
        "X_columns",
    ]

    for key in possible_feature_keys:
        if key in model_bundle:
            features = model_bundle[key]

            if isinstance(features, (list, tuple)):
                print(f"Daftar fitur ditemukan pada key: '{key}'")
                return list(features)

    return None

def get_model_features(model):
    """
    Mencoba mengambil nama fitur dari model.
    Cocok untuk model sklearn yang menyimpan feature_name_in_.
    """
    if hasattr(model, "feature_name_in_"):
        return list(model.feature_name_in_)
    
    if hasattr(model, "named_steps"):
        for step_name, step in model.named_steps.items():
            if hasattr(step, "feature_name_in_"):
                return list(step.feature_name_in_)
            
    return None

def get_model_classes(model):
    """
    Mengambil daftar class dari model/pipeline.
    Berguna untuk membaca urutan predict_proba().
    """
    if hasattr(model, "classes_"):
        return list(model.classes_)

    if hasattr(model, "named_steps"):
        for step_name, step in model.named_steps.items():
            if hasattr(step, "classes_"):
                return list(step.classes_)

    return None

def main():
    print("=== Manual Test Predict v1.2.0 ===")

    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model tidak ditemukan: {MODEL_PATH}")
    
    print(f"Load model dari: {MODEL_PATH}")
    loaded_object = joblib.load(MODEL_PATH)

    print(f"Tipe object yang di-load: {type(loaded_object)}")

    model = loaded_object
    features = None

    if isinstance(loaded_object, dict):
        inspect_dict_model(loaded_object)

        model = find_model_from_dict(loaded_object)
        features = find_features_from_dict(loaded_object)

        if model is None:
            print("\nModel sklearn tidak ditemukan di dalam dictionary.")
            print("Cek key dictionary di atas untuk mengetahui struktur file model.")
            return

    if features is None:
        print("\nModel berhasil di-load, tetapi nama fitur tidak ditemukan otomatis.")
        print("Silakan cek kembali fitur training yang digunakan pada v.1.0.1.")
        return
    
    if features is None:
        features = get_model_features(model)

    print(f"\nTipe model sebenarnya: {type(model)}")
    
    if features is None:
        print("\nModel berhasil ditemukan, tetapi daftar fitur belum ditemukan.")
        print("Artinya kita perlu cek kembali file training v1.0.1 untuk melihat fitur input yang digunakan.")
        return

    print("\nFitur yang dibutuhkan model:")
    for idx, feature in enumerate(features, start=1):
        print(f"{idx}. {feature}")

    sample_data = {feature: [0] for feature in features}
    sample_df = pd.DataFrame(sample_data)

    print("\nSample input:")
    print(sample_df)

    prediction = model.predict(sample_df)

    print("\nHasil prediksi:")
    print(prediction)

    if hasattr(model, "predict_proba"):
        probability = model.predict_proba(sample_df)
        classes = get_model_classes(model)

        print("\nProbabilitas prediksi:")
        print(probability)

        if classes is not None:
            print("\nProbabilitas per class:")
            for label, prob in zip(classes, probability[0]):
                print(f"{label}: {prob:.4f}")

    print("\nManual test predict selesai.")


if __name__ == "__main__":
    main()