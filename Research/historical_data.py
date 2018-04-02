import requests
import time
from config import ccc_credentials
from coins import coin_ids

data_types = ["price", "marketCap", "tradeVolume", "priceSentiment"]

# get starting date for each coin
def get_starting_dates(session_object):
    result = {}
    for coin in coin_ids:
        print("Issuing request for starting date of {}".format(coin['name']))
        r = session_object.get("https://www.cryptocurrencychart.com/api/coin/view/{}/".format(coin["id"]))
        if r.status_code == 200:
            result[coin['name']] = r.json()['firstData']
            print("Starting date for {} = {}".format(coin['name'], result[coin['name']]))
            time.sleep(1)
        else:
            print("Error occurred")
            print(str(r))
    return result

def get_coin_data(session_object, coin, startDate):
    for data_type in data_types:
        r = session_object.get("https://www.cryptocurrencychart.com/api/coin/history/{}/{}/{}/{}".format(
            coin['id'], startDate, endDate, data_type))
        if r.status_code == 200:
            # TODO: put data in database

def init():
    s = requests.Session()
    s.headers.update({ 'Key': ccc_credentials['api_key'], 'Secret': ccc_credentials['api_secret'] })

    dates = get_starting_dates(s)
    for coin in coin_ids:
        get_coin_data(s, coin, dates[coin['name']])
