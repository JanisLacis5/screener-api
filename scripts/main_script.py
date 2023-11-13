from concurrent.futures import ThreadPoolExecutor
from functions import get_eastern_time
from yahooquery import Ticker
import pandas as pd
from prepare_stocks import prepare_stocks

data = prepare_stocks()
# stocks_to_watch = data['symbol'].tolist()

# while True:
