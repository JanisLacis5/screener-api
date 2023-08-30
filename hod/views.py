import requests


def send_hod_data(data):
    url = 'http://localhost:3000/api/hod-screener-data'
    res = requests.post(url, json=data)
    res = res.json()
    if res['message'] == 'success':
        return
    print(res['message'])
