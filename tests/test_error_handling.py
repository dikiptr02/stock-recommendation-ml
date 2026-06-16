from app.routes import prediction_routes as prediction_route
from app.services.model_loader import ModelLoaderError


def _valid_prediction_payload():
    return {
        "Daily_Return": 0.01,
        "MA_5": 6100.0,
        "MA_10": 6050.0,
        "RSI": 55.0,
        "Volatility": 0.02,
        "Volume_Change": 0.15,
    }


def test_not_found_error_returns_standard_json(client):
    response = client.get("/endpoint-yang-tidak-ada")

    assert response.status_code == 404

    data = response.json()

    assert data["status"] == "error"
    assert data["message"] == "Not Found"
    assert data["errors"] == []


def test_model_loader_error_returns_flat_json_response(client, monkeypatch):
    def fake_predict(input_data):
        raise ModelLoaderError("Forced model error for testing.")

    monkeypatch.setattr(prediction_route.model_loader, "predict", fake_predict)

    response = client.post(
        "/api/v1/predict",
        json=_valid_prediction_payload(),
    )

    assert response.status_code == 500

    data = response.json()

    assert "detail" not in data
    assert data["status"] == "error"
    assert data["message"] == "Model prediction failed."
    assert data["errors"][0]["field"] is None
    assert data["errors"][0]["message"] == "Forced model error for testing."
    assert data["errors"][0]["value"] is None