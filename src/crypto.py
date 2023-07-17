import requests
import pandas as pd
import datetime

def check_available(coin_id: str):
    response = requests.get(f"https://api.coingecko.com/api/v3/coins/list")
    return coin_id in [asset["id"] for asset in response.json()]

def get_name(coin_id: str) -> str:
    if check_available(coin_id):
        response = requests.get(f"https://api.coingecko.com/api/v3/coins/{coin_id}")
        return response.json()["name"]

def get_price(coin_id: str, vs_currency="usd", days="max", interval="daily"):
    if check_available(coin_id):
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
        payload = {"vs_currency": vs_currency, "days": days, "interval": interval}
        response = requests.get(url, params=payload)
        data = response.json()
        
        timestamp_list, price_list = [], []
        for price in data["prices"]:
            timestamp_list.append(datetime.datetime.fromtimestamp(price[0]/1000))
            price_list.append(price[1])
            
        return timestamp_list, price_list
