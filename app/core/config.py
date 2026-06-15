APP_NAME = "Stock Recommendation Prediction API"
APP_VERSION = "1.5.0"
API_PREFIX = "/api/v1"

MODEL_VERSION_FALLBACK = "v1.0.1"

DEFAULT_PERIOD = "5y"
ALLOWED_PERIODS = {"1y", "5y", "max"}

MAX_BATCH_TICKERS = 10

FEATURE_COLUMNS = [
    "Daily_Return",
    "MA_5",
    "MA_10",
    "RSI",
    "Volatility",
    "Volume_Change",
]