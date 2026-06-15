def test_predict_endpoint_missing_required_field(client):
    payload = {
        "Daily_Return": 0.01,
        "MA_5": 6100.0,
        "MA_10": 6050.0,
        "RSI": 55.0,
        "Volatility": 0.02
        # Volume_Change sengaja tidak dikirim
    }

    response = client.post("/api/v1/predict", json=payload)

    assert response.status_code == 422

def test_predict_endpoint_invalid_data_type(client):
    payload = {
        "Daily_Return": "not-a-float",
        "MA_5": 6100.0,
        "MA_10": 6050.0,
        "RSI": 55.0,
        "Volatility": 0.02,
        "Volume_Change": 0.15
    }

    response = client.post("/api/v1/predict", json=payload)

    assert response.status_code == 422