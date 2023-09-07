from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from time import perf_counter
import pytz
from yahooquery import Ticker
import pandas as pd
from prepare_stocks import make_series
from hod.views import send_hod_data, download_file


def fetch_price(stock):
    try:
        return {stock: Ticker(stock).price[stock]["regularMarketDayHigh"]}
    except TypeError as e:
        print(f"there was a type error = {e}, on stock = {stock}")
        pass
    except KeyError as e:
        print(f"there was a key error = {e}, on stock = {stock}")
        pass


def get_stock_price(stocks):
    start = perf_counter()  # TEMP

    with ThreadPoolExecutor(max_workers=6) as executor:
        full_price_data = pd.Series(
            {
                list(item.keys())[0]: list(item.values())[0]
                for item in executor.map(fetch_price, stocks)
                if item is not None
            }
        )

    end = perf_counter()  # TEMP
    # print(end - start)  #TEMP

    return full_price_data


def get_blank_fields(stock):
    float = Ticker(stock).key_stats[stock]['floatShares']
    volume = Ticker(stock).price[stock]['regularMarketVolume']
    rel_volume = volume / Ticker(stock).price[stock]['averageDailyVolume10Day']
    return {
        'float': float,
        'volume': volume,
        'rel_volume': rel_volume
    }


def find_hod_prices(stocks, old_data):
    new_data = get_stock_price(stocks)

    for stock in stocks:
        if old_data[stock] < new_data[stock]:
            stats = get_blank_fields(stock)
            float_shares, volume, rel_volume = stats['float'], stats['volume'], stats['rel_volume']
            old_data[stock] = new_data[stock]
            print("sending data")
            data = {'time': get_eastern_time(), 'stock': stock, 'price': new_data[stock], 'float': float_shares,
                    'volume': volume, 'relVolume': rel_volume}
            send_hod_data(data=data)

    return new_data


def get_eastern_time():
    est_timezone = pytz.timezone("America/New_York")
    est_time = datetime.now(est_timezone)
    est_time = est_time.strftime("%H%M")
    return est_time


download_file()
print("downloaded file")  # TEMP

data = make_series()
stocks_to_watch = list(data.index)

while True:
    # print("starting while loop")
    temp_time = str(datetime.now())  # TEMP

    # refresh stock array each hour
    time = get_eastern_time()
    if int(time) % 100 == 0:
        download_file()
        stocks_to_watch = make_series()

    data = find_hod_prices(stocks_to_watch, data)

    # print(f"while loop done, time now: {temp_time[11:19]}")  # TEMP
