from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from time import perf_counter
import pytz
from yahooquery import Ticker
import pandas as pd
from .views import say_hi
from django.http import HttpResponse



def get_stock_price(stocks):
    start = perf_counter()

    def fetch_price(stock):
        return {stock: Ticker(stock).price[stock]['regularMarketDayHigh']}

    with ThreadPoolExecutor(max_workers=2) as executor:
        full_price_data = pd.Series({
            list(item.keys())[0]: list(item.values())[0]
            for item in executor.map(fetch_price, stocks)
        })

    end = perf_counter()
    # print(end - start)

    return full_price_data


def find_hod_prices(stocks, old_data, stocks_to_watch):
    new_data = get_stock_price(stocks_to_watch)

    for stock in stocks:
        if old_data[stock] < new_data[stock]:
            data = {stock: new_data[stock]}
            print(data)
            say_hi(data=data)

    return new_data

def main():
    HttpResponse('hello')
    # get eastern time
    est_timezone = pytz.timezone("America/New_York")
    est_time = datetime.now(est_timezone)
    est_time = est_time.strftime("%H:%M")

    # get all the tickers that are in my prefered price range and add to the stocks_to_watch list
    # stocks_to_watch = list()
    #
    # with open('ticker-list.csv') as f:
    #     # skip header line in file
    #     next(f)
    #
    #     # filtering and appending process
    #     for line in f:
    #         line_split = line.split(',')
    #         ticker = line_split[0]
    #         price = float(line_split[2][1:])
    #         if 2 < price < 50:
    #             stocks_to_watch.append(ticker)
    #
    stocks_to_watch = ['MSFT', 'TSLA', 'AAPL', 'VFS']
    starting_data = get_stock_price(tuple(stocks_to_watch))
    data = find_hod_prices(stocks_to_watch, starting_data, stocks_to_watch)

    while True:
        time = str(datetime.now())

        data = find_hod_prices(stocks_to_watch, data, stocks_to_watch)
        # print(f'while loop done, time now: {time[11:19]}')
