from stock import Stock
from user import User
from gui import create_app
import tkinter as tk

def main():
    username = input("Введите ваше имя пользователя: ")
    initial_balance = 1000000

    stocks = {
        "бтк": Stock("бтк", "bitcoin"),
        "эфир": Stock("эфир", "ethereum")
    }

    root = tk.Tk()
    balance_label = tk.Label(root, text=f"Баланс: ${initial_balance:.2f}", font=("Arial", 16))
    balance_label.pack(pady=10)

    user = User(username, initial_balance, balance_label, stocks)


    create_app(user, stocks, root)

if __name__ == "__main__":
    main()
