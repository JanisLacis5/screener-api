from yahooquery import Ticker
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
from sql_connection import create_server_connection


# GETTING STOCKS FROM DB

# def prepare_stocks():
#     return_list = list()
#     conn = create_server_connection(r'DESKTOP-4C6G875\MSSQLSERVER03', 'stocksDB', 'root', 'root')
#     cursor = conn.cursor()
#
#     table = cursor.execute('SELECT * FROM stocks')
#
#     columns = ['symbol', 'price', 'dayChange', 'floatShares', 'volume', 'relVolume']
#     table_df = pd.DataFrame.from_records(list(table), columns=columns)
#     table_df.reset_index()
#
#     for row, stock in table_df.iterrows():
#         if 2 < stock['floatShares'] < 30 and stock['volume'] > 500_000 and stock['dayChange'] > 5:
#             return_list.append(stock)
#
#     return return_list

def prepare_stocks():
    return_list = list()

    stocks = pd.read_csv('./ticker-list.csv')
    stocks.reset_index()

    for row, stock in stocks.iterrows():
        float_shares = Ticker(stock['symbol']).key_stats[stock['symbol']]['floatShares']
        if float_shares < 50_000_000 and int(stock['volume']) > 500_000 and float(stock['pctchange'][:-1]) > 5:
            return_list.append(stock['symbol'])

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
