#! /usr/bin/env python
# -*- coding: utf-8 -*-

from  flask import Flask
import requests
from time import sleep

import misc
import openweathermap


MAIN_URL = f'https://api.telegram.org/bot{misc.TOKEN}/'
global last_update_id
last_update_id = 0


def get_updates():
    url = MAIN_URL + 'getUpdates'
    r = requests.get(url)
    return r.json()


def get_message():
    data = get_updates()
    last_object = data['result'][-1]
    current_update_id = last_object['update_id']
    global last_update_id
    if last_update_id != current_update_id:
        last_update_id = current_update_id
        chat_id = last_object['message']['chat']['id']
        text = last_object['message']['text']
        message_data = {'chat_id': chat_id,
                   'text': text}
        return message_data
    return None


def send_message(chat_id, text='No data'):
    url = MAIN_URL + f'sendMessage?chat_id={chat_id}&text={text}'
    r = requests.get(url)


def main():
    while True:
        message = get_message()
        if message != None:
            chat_id = message['chat_id']
            text = message['text']
            if 'weather' in text:
                send_message(chat_id, openweathermap.get_openweathermap())
        else:
            continue
        sleep(2)


if __name__ == '__main__':
    main()
