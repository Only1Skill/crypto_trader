import matplotlib.pyplot as plt


def plot_stock_prices(stock):
    plt.plot(stock.price_history, label=stock.name)
    plt.title(f"История цен: {stock.name}")
    plt.xlabel("Время")
    plt.ylabel("Цена")
    plt.legend()
    plt.show()
