from yahooquery import Ticker
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
from sql_conn import create_server_connection


# GETTING STOCKS FROM DB

def get_primary_stocks(cursor):
    table = cursor.execute('SELECT * FROM primaryStocks')

    columns = ['symbol', 'price', 'dayChange', 'floatShares', 'volume', 'relVolume']
    table_df = pd.DataFrame.from_records(list(table), columns=columns)
    table_df.reset_index()

    return table_df
