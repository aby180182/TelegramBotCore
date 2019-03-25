import requests
import json
from main import write_json


def get_usd():
    PB_URL = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
    r = requests.get(PB_URL).json()
    buy = round(float(r[0]['buy']), 2)
    sell = round(float(r[0]['sale']), 2)
    answer_string = 'usd/uah: buy: ' + str(buy) + ' sell: ' + str(sell)

    return answer_string



