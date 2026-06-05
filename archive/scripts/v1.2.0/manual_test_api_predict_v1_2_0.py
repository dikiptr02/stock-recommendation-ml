import json
import urllib.error
import urllib.request


API_URL = "http://127.0.0.1:8000/api/v1/predict"


def main():
    print("=== Manual Test Prediction API v1.2.0 ===")

    payload = {
        "Daily_Return": 0.012,
        "MA_5": 102.5,
        "MA_10": 101.8,
        "RSI": 55.2,
        "Volatility": 0.03,
        "Volume_Change": 0.12,
    }

    data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        API_URL,
        data=data,
        headers={
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request) as response:
            response_body = response.read().decode("utf-8")
            result = json.loads(response_body)

        print("\nRequest payload:")
        print(json.dumps(payload, indent=4))

        print("\nAPI response:")
        print(json.dumps(result, indent=4))

        print("\nManual test Prediction API selesai.")

    except urllib.error.HTTPError as error:
        print("\nAPI mengembalikan HTTP Error.")
        print(f"Status code: {error.code}")

        error_body = error.read().decode("utf-8")
        print("\nError response body:")
        print(error_body)

    except urllib.error.URLError as error:
        print("\nGagal menghubungi API.")
        print("Pastikan server FastAPI sudah berjalan dengan command:")
        print("uvicorn app.main:app --reload")
        print(f"\nDetail error: {error}")


if __name__ == "__main__":
    main()