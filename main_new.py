#! /usr/bin/env python
# -*- coding: utf-8 -*-

from  flask import Flask
from flask import request
from flask import jsonify

import requests
import json

import misc
import weather, forecast, currency, uku, work, rabota


app = Flask(__name__)


MAIN_URL = f'https://api.telegram.org/bot{misc.TOKEN}/'


def write_json(data, filename='answer.json'):
    with open(filename, 'w', encoding='utf-8', errors='ignore') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def get_updates():
    url = MAIN_URL + 'getUpdates'
    r = requests.get(url)
    return r.json()


def send_message(chat_id, text='No data'):
    url = MAIN_URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json=answer)
    return r.json()


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        chat_id = r['message']['chat']['id']
        user_message = r['message']['text']

        if 'weather' in user_message:
            send_message(chat_id, weather.get_weather_now())
        elif 'forecast' in user_message:
            send_message(chat_id, forecast.get_weather_forecast())
        elif 'usd' in user_message:
            send_message(chat_id, currency.get_usd())
        elif 'uku' in user_message:
            send_message(chat_id, uku.get_uku_data())
        elif 'work' in user_message:
            send_message(chat_id, work.get_work_data())
        elif 'rabota' in user_message:
            send_message(chat_id, rabota.get_rabota_data())

        return jsonify(r)
    return 'No data available yet!!!'


# https://api.telegram.org/bot647848111:AAEy2t2I-J0D4oK8CnTci7kvMmtTTkXa0EA/setWebhook?url=https://ab2b3039.ngrok.io/'

def main():
    # r = get_updates()
    # chat_id = r['result'][-1]['message']['chat']['id']
    # send_message(chat_id)

    pass


if __name__ == '__main__':
    app.run()
