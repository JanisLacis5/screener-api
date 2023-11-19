import pandas as pd
from yahooquery import Ticker
import yfinance as yf
import requests
from split_main_table import split_main_table
from sql_conn import create_server_connection
from update_tables import update_tables

conn = create_server_connection('LACIS', 'stocksDB', 'root', 'root')
cursor = conn.cursor()

# print(update_tables(cursor))
print(Ticker('aapl').price)
