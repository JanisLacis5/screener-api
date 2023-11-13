from yahooquery import Ticker
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
from sql_connection import create_server_connection


# GETTING STOCKS FROM DB

def prepare_stocks():
    conn = create_server_connection('LACIS', 'stocksDB', 'root', 'root')
    cursor = conn.cursor()

    table = cursor.execute('SELECT * FROM stocks where floatShares<? and volume>? and dayChange>? and price >?',
                           50_000_000, 250_000, 5, 1)

    columns = ['symbol', 'price', 'dayChange', 'floatShares', 'volume', 'relVolume']
    table_df = pd.DataFrame.from_records(list(table), columns=columns)
    table_df.reset_index()

    return table_df
