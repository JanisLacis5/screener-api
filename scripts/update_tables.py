from yahooquery import Ticker


def update_tables(cursor):
    # make lists from secondaryStocks and nonImportantStocks table
    secondary_table = [row for row in cursor.execute('SELECT ticker from secondaryStocks')]
    non_important_table = [row for row in cursor.execute('SELECT ticker from nonImportantStocks')]

    # get all data from api about stocks from previous step
    secondary_table_summary_data = Ticker(secondary_table).summary_detail
    secondary_table_key_stats = Ticker(secondary_table).key_stats
    non_important_table_summary_data = Ticker(non_important_table).key_stats
    non_important_table_key_stats = Ticker(non_important_table).key_stats

    return secondary_table
