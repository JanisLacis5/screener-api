from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from time import perf_counter
import pytz
from yahooquery import Ticker
import pandas as pd
from hod.views import download_file

data = download_file()
