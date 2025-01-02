import tkinter as tk
from tkinter import messagebox


class User:
    def __init__(self, username: str, balance: float, balance_label: tk.Label, stocks: dict):
        """
        Инициализирует объект User.

        :param username: Имя пользователя
        :param balance: Баланс пользователя
        :param balance_label: Виджет для отображения баланса
        :param stocks: Словарь акций
        """
        self.username = username
        self.balance = balance
        self.portfolio = {}
        self.balance_label = balance_label  # Виджет для отображения баланса
        self.stocks = stocks  # Доступные акции

    def buy_stock(self, stock, amount: int):
        """
        Покупает определённое количество акций.

        :param stock: Акция для покупки
        :param amount: Количество акций
        """
        total_price = stock.price * amount
        if self.balance < total_price:
            messagebox.showerror("Ошибка", "Недостаточно денег для покупки.")
            return
        self.balance -= total_price
        self.portfolio[stock.name] = self.portfolio.get(stock.name, 0) + amount
        messagebox.showinfo("Покупка", f"Вы купили {amount} акций {stock.name}.")
        self.update_balance_label()

    def sell_stock(self, stock, amount: int):
        """
        Продает определённое количество акций.

        :param stock: Акция для продажи
        :param amount: Количество акций
        """
        if stock.name not in self.portfolio or self.portfolio[stock.name] < amount:
            messagebox.showerror("Ошибка", "Недостаточно акций для продажи.")
            return

        total_price = stock.price * amount
        self.balance += total_price
        self.portfolio[stock.name] -= amount

        if self.portfolio[stock.name] == 0:
            del self.portfolio[stock.name]  # Удаляем акцию, если проданы все

        messagebox.showinfo("Продажа",
                            f"Вы продали {amount} акций {stock.name}. Ваш текущий баланс: ${self.balance:.2f}")
        self.update_balance_label()

    def check_portfolio(self):
        """
        Проверяет статус портфеля и отображает информацию.
        """
        total_value = self.balance
        portfolio_details = []

        for stock_name, amount in self.portfolio.items():
            stock_price = self.stocks[stock_name].price
            stock_value = stock_price * amount
            total_value += stock_value
            portfolio_details.append(f"{stock_name}: {amount}, стоимость: ${stock_value:.2f}")

        portfolio_message = "\n".join(portfolio_details)
        portfolio_message += f"\n\nОбщая стоимость активов: ${total_value:.2f}\nБаланс: ${self.balance:.2f}"
        messagebox.showinfo("Ваш портфель", portfolio_message if portfolio_details else "Портфель пуст.")

    def update_balance_label(self):
        """
        Обновляет отображение баланса на экране.
        """
        self.balance_label.config(text=f"Баланс: ${self.balance:.2f}")
