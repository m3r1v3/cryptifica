import requests
import pandas as pd
import datetime


def get_symbol(coin_id: str) -> str:
    response = requests.get(f"https://api.coincap.io/v2/assets/{coin_id}")
    return response.json()["data"]["symbol"]


def get_name(coin_id: str) -> str:
    response = requests.get(f"https://api.coincap.io/v2/assets/{coin_id}")
    return response.json()["data"]["name"]


def get_price(coin_id: str):
    response = requests.get(f"https://api.coincap.io/v2/assets/{coin_id}")
    return response.json()["data"]["priceUsd"]


def get_change_percent(coin_id: str):
    response = requests.get(f"https://api.coincap.io/v2/assets/{coin_id}")
    return response.json()["data"]["changePercent24Hr"]
