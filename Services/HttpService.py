import requests
from config import USD_API_KEY


def get_crypto_price(network):
    url = "https://min-api.cryptocompare.com/data/price"
    params = {
        "fsym": network,
        "tsyms": "USD",
        "api_key": USD_API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        price = data["USD"]
        return price
    else:
        print("Ошибка при получении данных:", response.status_code)
        return None
