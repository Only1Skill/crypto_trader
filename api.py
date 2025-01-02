import requests
import time


def get_crypto_price(symbol: str):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd'
    for _ in range(5):
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data[symbol]['usd']
        elif response.status_code == 429:
            print("Превышен лимит запросов. Ждём минуту...")
            time.sleep(60)
        else:
            print(f"Ошибка API: {response.status_code}")
    return None
