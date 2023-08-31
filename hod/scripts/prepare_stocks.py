from yahooquery import Ticker
from time import perf_counter
from concurrent.futures import ThreadPoolExecutor
import pandas as pd


def func(line):
    stock = line.split(',')[0].strip()
    if '^' in stock or '/' in stock:
        return
    price = Ticker(stock).price[stock]['regularMarketPrice']
    volume = Ticker(stock).price[stock]['regularMarketVolume']
    change = (Ticker(stock).price[stock]['regularMarketPreviousClose'] - Ticker(stock).price[stock][
        'regularMarketPrice']) / Ticker(stock).price[stock]['regularMarketPrice'] * 100

    if 2 < price < 30 and volume > 500_000 and change > 5:
        return {stock: Ticker(stock).price[stock]['regularMarketDayHigh']}
    return


def prepare_stocks():
    return_list = list()

    with open('../../ticker-list.csv') as f:
        next(f)
        start = perf_counter()
        with ThreadPoolExecutor(max_workers=6) as executor:
            data = {item for item in executor.map(func, f)}
        end = perf_counter()
        print(data)
        print(end - start)

    return return_list


def fetch_price(stock):
    try:
        return {stock: Ticker(stock).price[stock]['regularMarketDayHigh']}
    except TypeError as e:
        print(f'there was a type error = {e}, on stock = {stock}')
        pass
    except KeyError as e:
        print(f'there was a key error = {e}, on stock = {stock}')
        pass


def make_series():
    stocks = prepare_stocks()
    with ThreadPoolExecutor(max_workers=6) as executor:
        full_price_data = {item for item in executor.map(fetch_price, stocks) if item is not None}

    return pd.Series(full_price_data)


print(make_series())
