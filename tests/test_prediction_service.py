from app.services.prediction_service import (
    _get_start_date,
    _normalize_ticker,
    _normalize_tickers,
)


def test_normalize_ticker_trims_and_uppercases_value():
    result = _normalize_ticker(" bbca.jk ")

    assert result == "BBCA.JK"


def test_normalize_tickers_removes_duplicates_and_keeps_order():
    result = _normalize_tickers([
        "bbca.jk",
        " tlkm.jk ",
        "BBCA.JK",
        "asii.jk",
    ])

    assert result == ["BBCA.JK", "TLKM.JK", "ASII.JK"]


def test_get_start_date_returns_date_string():
    result = _get_start_date("1y")

    assert isinstance(result, str)
    assert len(result) == 10
    assert result.count("-") == 2