from yahooquery import Ticker
from time import perf_counter
from concurrent.futures import ThreadPoolExecutor
import pandas as pd


def prepare_stocks():
    return_list = list()

    with open('ticker-list.csv') as f:
        next(f)
        for line in f:
            split_line = line.split(',')
            stock = split_line[0].strip()
            if '^' in stock or '/' in stock:
                continue
            price = split_line[2].strip()
            change = split_line[4].strip()
            volume = split_line[8].strip()
            if 2 < float(price[1:]) < 30 and int(volume) > 500_000 and float(change[:-1]) > 5:
                return_list.append(stock)
        print(len(return_list))

    return return_list


def make_series():
    stocks = prepare_stocks()

    def fetch_price(stock):
        try:
            return {stock: Ticker(stock).price[stock]['regularMarketDayHigh']}
        except TypeError as e:
            print(f'there was a type error = {e}, on stock = {stock}')
            pass
        except KeyError as e:
            print(f'there was a key error = {e}, on stock = {stock}')
            pass

    with ThreadPoolExecutor(max_workers=6) as executor:
        full_price_data = {list(item.keys())[0]: list(item.values())[0] for item in executor.map(fetch_price, stocks)}

    return pd.Series(full_price_data)
