def test_predict_endpoint_valid_input(client):
    payload = {
        "Daily_Return": 0.01,
        "MA_5": 6100.0,
        "MA_10": 6050.0,
        "RSI": 55.0,
        "Volatility": 0.02,
        "Volume_Change": 0.15,
    }

    response = client.post("/api/v1/predict", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["prediction"] in ["Buy", "Hold", "Sell"]
    assert isinstance(data["confidence"], float)
    assert isinstance(data["probabilities"], dict)
    assert "Buy" in data["probabilities"]
    assert "Hold" in data["probabilities"]
    assert "Sell" in data["probabilities"]