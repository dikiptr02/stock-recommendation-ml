from unittest.mock import MagicMock, patch

MOCK_TICKER_RESULT = {
    "status": "success",
    "ticker": "BBCA.JK",
    "period": "1y",
    "model_version": "v1.0.1",
    "model_name": "RandomForestClassifier",
    "latest_data_date": "2024-01-01",
    "latest_close_price": 9500.0,
    "features_used": {
        "Daily_Return": 0.01,
        "MA_5": 9400.0,
        "MA_10": 9300.0,
        "RSI": 55.0,
        "Volatility": 0.02,
        "Volume_Change": 0.1,
    },
    "recommendation": "Buy",
    "confidence": 0.75,
    "probabilities": {"Buy": 0.75, "Hold": 0.20, "Sell": 0.05},
}


def test_predict_ticker_valid(client):
    with patch(
        "app.routes.prediction_routes.predict_by_ticker",
        return_value=MOCK_TICKER_RESULT,
    ):
        response = client.post(
            "/api/v1/predict/ticker",
            json={"ticker": "BBCA.JK", "period": "1y"},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["ticker"] == "BBCA.JK"
    assert data["recommendation"] in ["Buy", "Hold", "Sell"]
    assert isinstance(data["confidence"], float)


def test_predict_ticker_invalid_format(client):
    response = client.post(
        "/api/v1/predict/ticker",
        json={"ticker": "!!!"},
    )

    assert response.status_code == 422
    data = response.json()
    assert data["status"] == "error"


def test_predict_ticker_empty_string(client):
    response = client.post(
        "/api/v1/predict/ticker",
        json={"ticker": ""},
    )

    assert response.status_code == 422


def test_predict_ticker_invalid_period(client):
    response = client.post(
        "/api/v1/predict/ticker",
        json={"ticker": "BBCA.JK", "period": "10y"},
    )

    assert response.status_code == 422