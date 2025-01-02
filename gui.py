import tkinter as tk
from tkinter import messagebox


def create_app(user, stocks, root):
    global stock_name_entry, amount_entry

    def buy_stock():
        stock_name = stock_name_entry.get().strip()
        if stock_name not in stocks:
            messagebox.showerror("Ошибка", "Акция не найдена.")
            return
        try:
            amount = int(amount_entry.get())
            user.buy_stock(stocks[stock_name], amount)
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректное количество.")

    def sell_stock():
        stock_name = stock_name_entry.get().strip()
        if stock_name not in stocks:
            messagebox.showerror("Ошибка", "Акция не найдена.")
            return
        try:
            amount = int(amount_entry.get())
            user.sell_stock(stocks[stock_name], amount)
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректное количество.")

    def check_portfolio():
        user.check_portfolio()

    def update_prices():
        for stock in stocks.values():
            new_price = stock.update_price()
            if new_price:
                messagebox.showinfo("Обновление", f"Обновлённая цена: {stock.name} = ${new_price:.2f}")

    def show_report():
        report_data = "\n".join(f"{stock.name}: {stock.price_history}" for stock in stocks.values())
        messagebox.showinfo("Отчет по активам", report_data if report_data else "Нет данных для отчета.")

    tk.Label(root, text="Криптовалюта:", font=("Arial", 12)).pack()
    stock_name_entry = tk.Entry(root)
    stock_name_entry.pack(pady=5)

    tk.Label(root, text="Количество:", font=("Arial", 12)).pack()
    amount_entry = tk.Entry(root)
    amount_entry.pack(pady=5)

    tk.Button(root, text="Купить", command=buy_stock, width=20).pack(pady=5)
    tk.Button(root, text="Продать", command=sell_stock, width=20).pack(pady=5)
    tk.Button(root, text="Проверить портфель", command=check_portfolio, width=20).pack(pady=5)
    tk.Button(root, text="Обновить цены", command=update_prices, width=20).pack(pady=5)
    tk.Button(root, text="Показать отчет", command=show_report, width=20).pack(pady=5)

    root.mainloop()
