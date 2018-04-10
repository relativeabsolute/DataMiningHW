import requests
import time
from config import ccc_credentials
from coins import coin_ids
from datetime import date
import sqlite3

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

def get_coin_data_range(session_object, coin, start_date, end_date, data_type):
    r = session_object.get("https://www.cryptocurrencychart.com/api/coin/history/{}/{}/{}/{}".format(
        coin['id'], start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), data_type))
    if r.status_code == 200:
        return r.json()['data']
    else:
        print("Error occurred!")
        print(r.text)
        return None
        
def get_coin_data(session_object, coin, start_date):
    result = {}
    end_date = date.today()
    delta = end_date - start_date
    for i in range(delta.days + 1):
        result[(start_date + timedelta(days=i)).strftime('%Y-%m-%d')] = {}
    for data_type in data_types:
        print("\tRequesting {}".format(data_type))
        # NOTE: will get a 500 if date range is more than a year apart
        range_start = ""
        range_end = ""
        for i in range(delta.days // 365):
            range_end = end_date - timedelta(days=365) * i
            range_start = range_end - timedelta(days=364)
            data = get_coin_data_range(session_object, coin, range_start, range_end, data_type)
            for item in data:
                result[item['date']][data_type] = item[data_type]
            time.sleep(1)
        # do request from start_date to range_start - 1 day
        data = get_coin_data_range(session_object, coin, start_date, range_start - timedelta(days=1), data_type)
        for item in data:
                result[item['date']][data_type] = item[data_type]
    return result

def write_data_to_db(data):
    conn = sqlite3.connect('coins.db')

    c = conn.cursor()

    c.execute("select name, coin_id from coins")
    name_ids = {item[0] : item[1] for item in c.fetchall()}
    for name, id in name_ids.items():
        for date, data in data[name]
            # TODO: finish!


def init():
    s = requests.Session()
    s.headers.update({ 'Key': ccc_credentials['api_key'], 'Secret': ccc_credentials['api_secret'] })
    coins_data = {}
    dates = get_starting_dates(s)
    for coin in coin_ids:
        print("Requesting data for {}\n".format(coin['name']))
        coins_data[coin['name']] = get_coin_data(s, coin, dates[coin['name']])
