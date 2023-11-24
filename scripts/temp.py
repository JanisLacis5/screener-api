from yahooquery import Ticker
from db_scripts.sql_conn import create_server_connection

conn = create_server_connection('LACIS', 'stocksDB', 'root', 'root')
cursor = conn.cursor()

# print(update_tables(cursor))
print(Ticker('aapl').price)
