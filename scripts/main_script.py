from prepare_stocks import get_primary_stocks
from db_scripts.sql_conn import create_server_connection

# create connection with database
conn = create_server_connection('LACIS', 'stocksDB', 'root', 'root')
cursor = conn.cursor()

data = get_primary_stocks(cursor)
