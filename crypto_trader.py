import requests
import matplotlib.pyplot as plt
import time
import tkinter as tk
from tkinter import messagebox

class User:
    def __init__(self, username, balance):
        self.username = username
        self.balance = balance
        self.portfolio = {}

    def buy_stock(self, stock, amount):
        itog_price = stock.price * amount
        if self.balance < itog_price:
            messagebox.showerror("Ошибка", "Недостаточно денег для покупки.")
            return
        self.balance -= itog_price
        if stock.name in self.portfolio:
            self.portfolio[stock.name] += amount
        else:
            self.portfolio[stock.name] = amount
        messagebox.showinfo("Покупка", f"Вы купили {amount} акций {stock.name}.")
        self.update_balance_label()

    def sell_stock(self, stock, amount):
        if stock.name not in self.portfolio or self.portfolio[stock.name] < amount:
            messagebox.showerror("Ошибка", "Недостаточно акций для продажи.")
            return
        itog_price = stock.price * amount
        self.balance += itog_price
        self.portfolio[stock.name] -= amount
        if self.portfolio[stock.name] == 0:
            del self.portfolio[stock.name]
        messagebox.showinfo("Продажа", f"Вы продали {amount} акций {stock.name}. Ваш текущий баланс: ${self.balance:.2f}")
        self.update_balance_label()

    def check_portfolio(self):
        total_value = self.balance
        portfolio_details = []
        for stock_name, amount in self.portfolio.items():
            stock_price = stocks[stock_name].price
            stock_value = stock_price * amount
            total_value += stock_value
            portfolio_details.append(f"{stock_name}: {amount}, стоимость: ${stock_value:.2f}")

        portfolio_message = "\n".join(portfolio_details)
        portfolio_message += f"\n\nОбщая стоимость активов: ${total_value:.2f}\nБаланс: ${self.balance:.2f}"
        messagebox.showinfo("Ваш портфель", portfolio_message if portfolio_details else "Портфель пуст.")

    def update_balance_label(self):
        balance_label.config(text=f"Баланс: ${self.balance:.2f}")


class Stock:
    def __init__(self, name, symbol):
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
        return None


def get_crypto_price(symbol):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd'
    for _ in range(5):
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data[symbol]['usd']
        elif response.status_code == 429:
            print("Превышен лимит запросов. Ожидание...")
            time.sleep(60)
        else:
            print(f"Ошибка при получении данных: {response.status_code}")
            return None
    return None


def plot_stock_prices(stock):
    plt.plot(stock.price_history, label=stock.name)
    plt.title(f"История цен {stock.name}")
    plt.xlabel("Время")
    plt.ylabel("Цена")
    plt.legend()
    plt.show()


def buy_stock():
    stock_name = stock_name_entry.get()
    try:
        amount = int(amount_entry.get())
        if amount <= 0:
            raise ValueError("Количество акций должно быть положительным")
        if stock_name not in stocks:
            messagebox.showerror("Ошибка", "Некорректное название криптовалюты.")
            return
        user.buy_stock(stocks[stock_name], amount)
    except ValueError as e:
        messagebox.showerror("Ошибка", str(e))


def sell_stock():
    stock_name = stock_name_entry.get()
    try:
        amount = int(amount_entry.get())
        if amount <= 0:
            raise ValueError("Количество акций должно быть положительным")
        if stock_name not in stocks:
            messagebox.showerror("Ошибка", "Некорректное название криптовалюты.")
            return
        user.sell_stock(stocks[stock_name], amount)
    except ValueError as e:
        messagebox.showerror("Ошибка", str(e))


def check_portfolio():
    user.check_portfolio()


def update_prices():
    for stock in stocks.values():
        new_price = stock.update_price()
        if new_price:
            messagebox.showinfo("Обновление", f"Цена {stock.name} обновлена: ${new_price:.2f}")


def show_report():
    report_data = "\n".join(f"{stock.name}: {stock.price_history}" for stock in stocks.values())
    messagebox.showinfo("Отчет по активам", report_data if report_data else "Нет данных для отчета.")


def main():
    global user, stocks, stock_name_entry, amount_entry, balance_label


    username = input("Введите ваше имя пользователя: ")
    user = User(username, 1000000)


    stocks = {
        "бтк": Stock("бтк", "bitcoin"),
        "эфир": Stock("эфир", "ethereum")
    }


    root = tk.Tk()
    root.title("КриптоТрейдер")
    root.geometry("400x400")

    balance_label = tk.Label(root, text=f"Баланс: ${user.balance:.2f}", font=("Arial", 16))
    balance_label.pack(pady=10)

    tk.Label(root, text="Название криптовалюты:", font=("Arial", 12)).pack(pady=5)
    stock_name_entry = tk.Entry(root)
    stock_name_entry.pack(pady=5)

    tk.Label(root, text="Количество акций:", font=("Arial", 12)).pack(pady=5)
    amount_entry = tk.Entry(root)
    amount_entry.pack(pady=5)

    tk.Button(root, text="Купить", command=buy_stock, width=20).pack(pady=5)
    tk.Button(root, text="Продать", command=sell_stock, width=20).pack(pady=5)
    tk.Button(root, text="Проверить портфель", command=check_portfolio, width=20).pack(pady=5)
    tk.Button(root, text="Обновить цены", command=update_prices, width=20).pack(pady=5)
    tk.Button(root, text="Показать отчет", command=show_report, width=20).pack(pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()
