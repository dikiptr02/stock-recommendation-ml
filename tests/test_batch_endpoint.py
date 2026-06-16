from unittest.mock import patch


MOCK_BATCH_RESULT = {
    "status": "success",
    "total_requested": 2,
    "total_success": 2,
    "total_failed": 0,
    "results": [
        {
            "ticker": "BBCA.JK",
            "status": "success",
            "message": None,
            "latest_data_date": "2024-01-01",
            "latest_close_price": 9500.0,
            "recommendation": "Buy",
            "confidence": 0.75,
            "probabilities": {"Buy": 0.75, "Hold": 0.20, "Sell": 0.05},
        },
        {
            "ticker": "TLKM.JK",
            "status": "success",
            "message": None,
            "latest_data_date": "2024-01-01",
            "latest_close_price": 3800.0,
            "recommendation": "Hold",
            "confidence": 0.60,
            "probabilities": {"Buy": 0.25, "Hold": 0.60, "Sell": 0.15},
        },
    ],
}


MOCK_BATCH_PARTIAL_FAIL = {
    "status": "success",
    "total_requested": 2,
    "total_success": 1,
    "total_failed": 1,
    "results": [
        {
            "ticker": "BBCA.JK",
            "status": "success",
            "message": None,
            "latest_data_date": "2024-01-01",
            "latest_close_price": 9500.0,
            "recommendation": "Buy",
            "confidence": 0.75,
            "probabilities": {"Buy": 0.75, "Hold": 0.20, "Sell": 0.05},
        },
        {
            "ticker": "INVALID",
            "status": "error",
            "message": "Data untuk ticker INVALID kosong.",
            "latest_data_date": None,
            "latest_close_price": None,
            "recommendation": None,
            "confidence": None,
            "probabilities": None,
        },
    ],
}


def test_predict_batch_valid(client):
    with patch(
        "app.routes.prediction_routes.predict_batch",
        return_value=MOCK_BATCH_RESULT,
    ):
        response = client.post(
            "/api/v1/predict/batch",
            json={"tickers": ["BBCA.JK", "TLKM.JK"], "period": "1y"},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["total_requested"] == 2
    assert data["total_success"] == 2
    assert data["total_failed"] == 0
    assert len(data["results"]) == 2


def test_predict_batch_partial_fail(client):
    with patch(
        "app.routes.prediction_routes.predict_batch",
        return_value=MOCK_BATCH_PARTIAL_FAIL,
    ):
        response = client.post(
            "/api/v1/predict/batch",
            json={"tickers": ["BBCA.JK", "INVALID"], "period": "1y"},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["total_success"] == 1
    assert data["total_failed"] == 1
    assert data["results"][1]["status"] == "error"


def test_predict_batch_invalid_ticker_format(client):
    response = client.post(
        "/api/v1/predict/batch",
        json={"tickers": ["BBCA.JK", "!!!"], "period": "1y"},
    )

    assert response.status_code == 422
    data = response.json()
    assert data["status"] == "error"


def test_predict_batch_empty_list(client):
    response = client.post(
        "/api/v1/predict/batch",
        json={"tickers": [], "period": "1y"},
    )

    assert response.status_code == 422


def test_predict_batch_invalid_period(client):
    response = client.post(
        "/api/v1/predict/batch",
        json={"tickers": ["BBCA.JK"], "period": "10y"},
    )

    assert response.status_code == 422