import requests
from config import *

#coin_codes = ['BTC', 'ETH', 'XRP', 'BCH', 'LTC', 'EOS', 'ADA', 'XLM', 'NEO', 'MIOTA' ]

def init():
    r = requests.get('https://www.cryptocurrencychart.com/api/coin/list',
            headers = { 'Key': ccc_credentials['api_key'], 'Secret': ccc_credentials['api_secret'] })
    if r.status_code == 200:
        coins = [coin for coin in r.json()['coins'] if coin['name'] in coin_names]
        with open('coins.py', 'w') as coin_ids:
            coin_ids.write('coin_ids = [')
            for coin in coins:
                coin_ids.write('{}\n'.format(str(coin)))
            coin_ids.write(']')
            coin_ids.flush()
    else:
        print(str(r))

if __name__ == "__main__":
    init()
