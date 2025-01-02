from api import get_crypto_price


class Stock:
    def __init__(self, name: str, symbol: str):
        self.name = name
        self.symbol = symbol
        self.price = self.get_price_from_api()
        self.price_history = [self.price]

    def get_price_from_api(self):
        return get_crypto_price(self.symbol)

    def update_price(self):
        new_price = self.get_price_from_api()
        if new_price:
            self.price = new_price
            self.price_history.append(new_price)
        return new_price
