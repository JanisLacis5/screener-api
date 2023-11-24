from db_scripts.sql_conn import create_server_connection
from yahooquery import Ticker
from scripts.functions import get_eastern_time


def split_stocks():
    conn = create_server_connection('LACIS', 'stocksDB', 'root', 'root')
    cursor = conn.cursor()

    for symbol, price, dayChange, floatShares, volume, relVolume in cursor.execute('select * from stocks'):
        time_now = get_eastern_time()

        # GET PRICE DATA
        ticker_data = Ticker(symbol).price[symbol]
        pre_market_high = ticker_data['preMarketPrice']
        post_market_high = ticker_data['postMarketPrice']
        day_high = ticker_data['regularMarketDayHigh']

        # SPLIT INTO 3 PRIORITY TABLES
        if 1 < price < 20 and volume > 100_000 and floatShares < 20_000_000 and dayChange > 10:
            cursor.execute('insert into primaryStocks (ticker, price, dayChange, floatShares, volume, relVolume) '
                           'values (?, ?, ?, ?, ?, ?)', symbol, price, dayChange, floatShares, volume, relVolume)

        elif 1 < price < 50 and volume > 50_000 and dayChange > 5:
            cursor.execute(
                'insert into secondaryStocks (ticker, price, dayChange, floatShares, volume, relVolume) '
                'values (?, ?, ?, ?, ?, ?)', symbol, price, dayChange, floatShares, volume, relVolume)
        else:
            cursor.execute(
                'insert into nonImportantStocks (ticker, price, dayChange, floatShares, volume, relVolume) '
                'values (?, ?, ?, ?, ?, ?)', symbol, price, dayChange, floatShares, volume, relVolume)
        cursor.commit()

        # CHOOSE BETWEEN PREMARKET, POSTMARKET OR DAY AND UPDATE HIGH OF DAY PRICE
        if 1600 > time_now > 930:
            cursor.execute('update primaryStocks'
                           'set dayHigh=?'
                           'where ticker=?', day_high, symbol)
        elif time_now > 1600 or time_now < 930:
            cursor.execute('if dayHigh<?'
                           'update primaryStocks'
                           'set dayHigh=?'
                           'where ticker=?', post_market_high, post_market_high, symbol)
        else:
            cursor.execute('if dayHigh<?'
                           'update primaryStocks'
                           'set dayHigh=?'
                           'where ticker=?', pre_market_high, pre_market_high, symbol)
        cursor.commit()

    return


split_stocks()
