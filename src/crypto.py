import requests
import datetime


def get_data(coin_id: str):
    return requests.get(f"https://api.coincap.io/v2/assets/{coin_id}").json()["data"]


def get_prices(coin_id: str):
    data = requests.get(f"https://api.coincap.io/v2/assets/{coin_id}/history?interval=d1").json()["data"][-30:]

    time, price = [], []

    for i in data:
        time.append(str(datetime.datetime.fromtimestamp(i['time']//1000)))
        price.append(float(i['priceUsd']))
    return time, price
