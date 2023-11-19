from concurrent.futures import ThreadPoolExecutor
from functions import get_eastern_time
from yahooquery import Ticker
import pandas as pd
from prepare_stocks import get_primary_stocks
from sql_conn import create_server_connection

# create connection with database
conn = create_server_connection('LACIS', 'stocksDB', 'root', 'root')
cursor = conn.cursor()

data = get_primary_stocks(cursor)
