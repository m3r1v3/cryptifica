import requests


def get_data(coin_id: str):
    return requests.get(f"https://api.coincap.io/v2/assets/{coin_id}").json()["data"]
