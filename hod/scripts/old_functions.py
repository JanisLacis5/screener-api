from concurrent.futures import ThreadPoolExecutor
from functions import get_eastern_time
from yahooquery import Ticker
import pandas as pd
from prepare_stocks import prepare_stocks
from hod.views import send_hod_data


def get_blank_fields(stock):
    float_sh = Ticker(stock).key_stats[stock]['floatShares']
    volume = Ticker(stock).price[stock]['regularMarketVolume']
    rel_volume = volume / Ticker(stock).price[stock]['averageDailyVolume10Day']
    return {
        'float': float_sh,
        'volume': volume,
        'rel_volume': rel_volume
    }


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
    with ThreadPoolExecutor(max_workers=6) as executor:
        full_price_data = pd.DataFrame(
            {
                list(item.keys())[0]: list(item.values())[0]
                for item in executor.map(fetch_price, stocks)
                if item is not None
            }
        )

    return full_price_data


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
