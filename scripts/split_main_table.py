import pandas as pd


def split_main_table(cursor):
    # make dataframe with all stocks
    table = cursor.execute('SELECT * FROM stocks')
    columns = ['symbol', 'price', 'dayChange', 'floatShares', 'volume', 'relVolume']
    table_df = pd.DataFrame.from_records(list(table), columns=columns)
    table_df.reset_index()

    # organise stocks between 3 tables
    for i, row in table_df.iterrows():
        symbol, price, day_change, float_shares, volume, rel_volume = row['symbol'], row['price'], row['dayChange'], \
            row['floatShares'], row[
            'volume'], row['relVolume']

        table = 'nonImportantStocks'
        if 1 < price < 20 and day_change > 1 and volume > 50_000:
            table = 'primaryStocks'
        elif 1 < price < 50 and day_change > -5:
            table = 'secondaryStocks'

        cursor.execute(f'INSERT INTO {table} (ticker, price, dayChange, floatShares, volume, relVolume)'
                       f'VALUES (?,?,?,?,?,?)', symbol, price, day_change, float_shares, volume, rel_volume)
        cursor.commit()

        del table_df
    return
