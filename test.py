from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from time import perf_counter
import pytz
from yahooquery import Ticker
import pandas as pd


def fetch_price(stock):
    stock_data = Ticker(stock).price[stock]
    try:
        return {stock: (stock_data['regularMarketDayHigh'], stock_data['regularMarketVolume'])}
    except TypeError as e:
        print(f'there was a type error = {e}, on stock = {stock}')
        pass
    except KeyError as e:
        print(f'there was a key error = {e}, on stock = {stock}')
        pass


def get_stock_price(stocks):
    print('getting prices')
    start = perf_counter()  # TEMP

    with ThreadPoolExecutor(max_workers=6) as executor:
        full_price_data = pd.Series(
            {
                list(item.keys())[0]: list(item.values())[0]
                for item in executor.map(fetch_price, stocks)
                if item is not None
            })

    end = perf_counter()  # TEMP
    # print(end - start)  #TEMP

    return full_price_data


def find_hod_prices(stocks, old_data):
    new_data = get_stock_price(stocks)

    # send data
    for stock in stocks:
        if old_data[stock] < new_data[stock]:
            print('sending data')
            data = {stock: new_data[stock]}

    return new_data


def get_stocks():
    print('getting stocks')
    # get all the tickers that are in my prefered price range and add to the stocks_to_watch list
    stocks_to_watch = list()

    with open('ticker-list.csv') as f:
        # skip header line in file
        next(f)

        # filtering and appending process
        for line in f:
            line_split = line.split(',')
            ticker = line_split[0].strip()
            price = float(line_split[2][1:])
            volume = int(line_split[8].strip())
            if 2 < price < 50 and volume > 500_000 and '^' not in ticker and '/' not in ticker:
                stocks_to_watch.append(ticker)
    print(len(stocks_to_watch))
    starting_data = get_stock_price(tuple(stocks_to_watch))
    data = find_hod_prices(stocks_to_watch, starting_data)
    return {
        'stocks_to_watch': stocks_to_watch,
        'hod_data': data
    }


def get_eastern_time():
    est_timezone = pytz.timezone("America/New_York")
    est_time = datetime.now(est_timezone)
    est_time = est_time.strftime("%H%M")
    return est_time


data = get_stocks()
stocks_to_watch, data = data['stocks_to_watch'], data['hod_data']

while True:
    print('starting while loop')
    temp_time = str(datetime.now())  # TEMP

    # refresh stock array each hour
    time = get_eastern_time()
    if int(time) % 100 == 0:
        data = get_stocks()
        stocks_to_watch, data = data['stocks_to_watch'], data['hod_data']

    data = find_hod_prices(stocks_to_watch, data)

    print(f'while loop done, time now: {temp_time[11:19]}')  # TEMP
