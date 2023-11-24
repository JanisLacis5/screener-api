import pandas as pd


# GETTING STOCKS FROM DB

def get_primary_stocks(cursor):
    table = cursor.execute('SELECT * FROM primaryStocks')

    columns = ['symbol', 'price', 'dayChange', 'floatShares', 'volume', 'relVolume']
    table_df = pd.DataFrame.from_records(list(table), columns=columns)
    table_df.reset_index()

    return table_df
