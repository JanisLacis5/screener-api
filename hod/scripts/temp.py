from prepare_stocks import prepare_stocks
import pandas as pd
from yahooquery import Ticker
import yfinance as yf
import requests

# query2.finance.yahoo.com/v6/finance/quoteSummary/aapl?modules=price&formatted=false&lang=en-US&region=US&corsDomain=finance.yahoo.com

print(requests.get(
    'https://query2.finance.yahoo.com/v10/finance/quoteSummary/AAPL?modules=financialData&modules=quoteType&modules=defaultKeyStatistics&modules=assetProfile&modules=summaryDetail&ssl=true'))
