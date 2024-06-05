import numpy as np
import matplotlib.pyplot as plt
from binance.client import Client
from binance.enums import *

# Вставьте ваш API ключ и секрет сюда
api_key = 'czs8NPf9uo1va2Sg4HB5NCWFO7XGNtP8RPHWLWU8eWqNw0XhqjCsPhJreJfaEMhv'
api_secret = 'v0Onk3jFT4G5Q4vufMt3eDqT2r2cKKW4NoOQC53uLNSfjRcBHfqdmYBrHaFa3Udx'

# Создание клиента Binance
client = Client(api_key, api_secret)

def get_historical_klines(symbol, interval, start_str):
    """Получение исторических данных"""
    klines = client.get_historical_klines(symbol, interval, start_str)
    return klines

def calculate_fibonacci_levels(data):
    """Расчет уровней Фибоначчи"""
    max_price = max(data)
    min_price = min(data)
    diff = max_price - min_price
    levels = {
        '0.0%': max_price,
        '23.6%': max_price - 0.236 * diff,
        '38.2%': max_price - 0.382 * diff,
        '50.0%': max_price - 0.5 * diff,
        '61.8%': max_price - 0.618 * diff,
        '100.0%': min_price
    }
    return levels

def find_trade_signals(data, levels):
    """Поиск точек входа на основе уровней Фибоначчи"""
    signals = []
    for i in range(1, len(data)):
        if data[i-1] > levels['38.2%'] and data[i] <= levels['38.2%']:
            signals.append(('Buy', i))
        elif data[i-1] < levels['61.8%'] and data[i] >= levels['61.8%']:
            signals.append(('Sell', i))
    return signals

def plot_data(prices, fibonacci_levels, signals):
    """Построение графика с уровнями Фибоначчи и сигналами"""
    plt.figure(figsize=(14, 7))
    plt.plot(prices, label='Close Prices')

    # Добавляем уровни Фибоначчи
    for level in fibonacci_levels:
        plt.axhline(y=fibonacci_levels[level], color='r', linestyle='--', label=f'Fibonacci {level}')

    # Добавляем сигналы
    for signal in signals:
        plt.plot(signal[1], prices[signal[1]], 'go' if signal[0] == 'Buy' else 'ro', markersize=10, label=signal[0])

    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.title('Fibonacci Levels and Trade Signals')
    plt.legend()
    plt.show()

def main():
    symbol = 'BTCUSDT'
    interval = Client.KLINE_INTERVAL_1DAY
    start_str = '1 month ago UTC'

    # Получение исторических данных
    klines = get_historical_klines(symbol, interval, start_str)
    close_prices = np.array([float(kline[4]) for kline in klines])

    # Рассчет уровней Фибоначчи
    fibonacci_levels = calculate_fibonacci_levels(close_prices)

    # Поиск точек входа
    signals = find_trade_signals(close_prices, fibonacci_levels)

    # Вывод сигналов
    for signal in signals:
        print(f"Signal: {signal[0]} at index {signal[1]} (price: {close_prices[signal[1]]})")

    # Расчет примерного расстояния, которое пройдет цена
    price_range = max(close_prices) - min(close_prices)
    print(f"Approximate price range: {price_range}")

    # Построение графика
    plot_data(close_prices, fibonacci_levels, signals)

if __name__ == '__main__':
    main()
