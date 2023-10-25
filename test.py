from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from time import perf_counter
import pytz
from yahooquery import Ticker
import pandas as pd
from hod.views import download_file, send_hod_data
from hod.scripts.prepare_stocks import make_series

data = {'time': 123, 'stock': 'a', 'price': 5151.23, 'float': 312312374,
        'volume': 312398712414, 'relVolume': 3.321312414}
send_hod_data(data=data)
