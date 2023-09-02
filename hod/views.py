import requests
import pandas as pd


def send_hod_data(data):
    url = 'http://localhost:3000/api/hod-screener-data'
    res = requests.post(url, json=data)
    res = res.json()
    if res['message'] == 'success':
        return
    print(res['message'])


def download_file():
    url = 'https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&download=true'
    headers = {'Accept-Language': 'en-US,en;q=0.9',
               'Accept-Encoding': 'gzip, deflate, br',
               'User-Agent': 'Java-http-client/'}

    res = requests.get(url, headers=headers)
    json_data = res.json()

    df = pd.DataFrame(json_data['data']['rows'], columns=json_data['data']['headers'])
    df.to_csv('ticker-list.csv', index=False)
    return
