from prepare_stocks import prepare_stocks
from yahooquery import Ticker
import pandas as pd

t = Ticker('AAPL')

print(t.price)
