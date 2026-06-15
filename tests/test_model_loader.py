import pytest

from app.services.model_loader import ModelLoaderError, StockModelLoader


def test_model_loader_loads_model_successfully():
    loader = StockModelLoader()

    loader.load_model()

    assert loader.is_loaded is True
    assert loader.model is not None
    assert loader.model_bundle is not None
    assert loader.feature_columns is not None
    assert isinstance(loader.feature_columns, list)
    assert len(loader.feature_columns) > 0
    assert loader.version is not None
    assert loader.model_name is not None
    assert loader.target_column is not None


def test_model_loader_raises_error_when_file_not_found():
    loader = StockModelLoader(model_path="models/model_yang_tidak_ada.pkl")

    with pytest.raises(ModelLoaderError):
        loader.load_model()


def test_model_loader_predict_returns_expected_structure():
    loader = StockModelLoader()

    sample_input = {
        "Daily_Return": 0.01,
        "MA_5": 6100.0,
        "MA_10": 6050.0,
        "RSI": 55.0,
        "Volatility": 0.02,
        "Volume_Change": 0.15,
    }

    result = loader.predict(sample_input)

    assert "prediction" in result
    assert "confidence" in result
    assert "probabilities" in result

    assert result["prediction"] in ["Buy", "Hold", "Sell"]
    assert isinstance(result["confidence"], float)
    assert isinstance(result["probabilities"], dict)

    
def test_model_loader_predict_raises_error_when_input_incomplete():
    loader = StockModelLoader()

    incomplete_input = {
        "Daily_Return": 0.01,
        "MA_5": 6100.0,
        "MA_10": 6050.0,
        "RSI": 55.0,
        "Volatility": 0.02,
        # Volume_Change sengaja tidak dikirim
    }

    with pytest.raises(ModelLoaderError):
        loader.predict(incomplete_input)