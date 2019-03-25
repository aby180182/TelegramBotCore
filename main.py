#! /usr/bin/env python
# -*- coding: utf-8 -*-

from  flask import Flask
from flask import request
from flask import jsonify
from flask_sslify import SSLify

import requests
import json
from bs4 import BeautifulSoup


app = Flask(__name__)
sslify = SSLify(app)

TOKEN = '647848111:AAEy2t2I-J0D4oK8CnTci7kvMmtTTkXa0EA'
MAIN_URL = 'https://api.telegram.org/bot{}/'.format(TOKEN)


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


# Openweathermap Weather codes and corressponding emojis
thunderstorm = u'\U0001F4A8'    # Code: 200's, 900, 901, 902, 905
drizzle = u'\U0001F4A7'         # Code: 300's
rain = u'\U00002614'            # Code: 500's
snowflake = u'\U00002744'       # Code: 600's snowflake
snowman = u'\U000026C4'         # Code: 600's snowman, 903, 906
atmosphere = u'\U0001F301'      # Code: 700's foogy
clearSky = u'\U00002600'        # Code: 800 clear sky
fewClouds = u'\U000026C5'       # Code: 801 sun behind clouds
clouds = u'\U00002601'          # Code: 802-803-804 clouds general
hot = u'\U0001F525'             # Code: 904
defaultEmoji = u'\U0001F300'    # default emojis


def get_emoji(weatherID):
    if weatherID:
        if str(weatherID)[0] == '2' or weatherID == 900 or weatherID == 901 or weatherID == 902 or weatherID == 905:
            return thunderstorm
        elif str(weatherID)[0] == '3':
            return drizzle
        elif str(weatherID)[0] == '5':
            return rain
        elif str(weatherID)[0] == '6' or weatherID == 903 or weatherID == 906:
            return snowflake + ' ' + snowman
        elif str(weatherID)[0] == '7':
            return atmosphere
        elif weatherID == 800:
            return clearSky
        elif weatherID == 801:
            return fewClouds
        elif weatherID == 802 or weatherID == 803 or weatherID == 803:
            return clouds
        elif weatherID == 904:
            return hot
        else:
            return defaultEmoji  # Default emoji

    else:
        return defaultEmoji  # Default emoji

def get_weather_now():
    WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather?'
    WEATHER_API_KEY = 'e57e1ce3c757ee3e891e0723e2aeb112'
    WEATHER_CITY_ID = '702550'
    WEATHER_UNIT = 'metric'

    url = WEATHER_URL + f'id={WEATHER_CITY_ID}&APPID={WEATHER_API_KEY}&units={WEATHER_UNIT}'
    r = requests.get(url).json()
    # write_json(r)

    cod = r['cod']
    city = r['name']
    weather_id = r['weather'][0]['id']
    description = r['weather'][0]['description']
    # icon = r['weather'][0]['icon']
    temp = r['main']['temp']
    wind = r['wind']['speed']

    if cod == 200:
        answer_string = str(city) + ' now' + '\ntemprature: ' + str(temp) + '\N{DEGREE SIGN}C' + '\n' + str(
            description) + get_emoji(weather_id) + '\nwind: ' + str(wind) + ' m/c \n'
    else:
        answer_string = 'Sorry! No available data.'

    return answer_string


def get_weather_forecast():
    WEATHER_URL = 'http://api.openweathermap.org/data/2.5/forecast?'
    WEATHER_API_KEY = 'e57e1ce3c757ee3e891e0723e2aeb112'
    WEATHER_CITY_ID = '702550'
    WEATHER_UNIT = 'metric'

    url = WEATHER_URL + f'id={WEATHER_CITY_ID}&APPID={WEATHER_API_KEY}&units={WEATHER_UNIT}'
    r = requests.get(url).json()
    # write_json(r)
    forecast_indexes_list = [0, 1, 3, 7]
    forecast_list = []
    for i in forecast_indexes_list:
        cod = r['cod']
        city = r['city']['name']
        weather_id = r['list'][i]['weather'][0]['id']
        description = r['list'][i]['weather'][0]['description']
        # icon = r['weather'][i]['icon']
        temp = r['list'][i]['main']['temp']
        wind = r['list'][i]['wind']['speed']
        data = {
            'cod': cod,
            'city': city,
            'weather_id': weather_id,
            'description': description,
            'temp': temp,
            'wind': wind
        }
        forecast_list.append(data)

    if forecast_list[0]['cod'] == "200":
        answer_string = str(forecast_list[0]['city']) + ' 3 hours' + '\ntemprature: ' + str(forecast_list[0]['temp'])\
                        + '\N{DEGREE SIGN}C' + '\n' + str(forecast_list[0]['description']) + get_emoji(forecast_list[0]['weather_id'])\
                        + '\nwind: ' + str(forecast_list[0]['wind']) + ' m/c \n---------------\n'\
                        + str(forecast_list[1]['city']) + ' 6 hours' + '\ntemprature: ' + str(forecast_list[1]['temp'])\
                        + '\N{DEGREE SIGN}C' + '\n' + str(forecast_list[1]['description']) + get_emoji(forecast_list[1]['weather_id'])\
                        + '\nwind: ' + str(forecast_list[1]['wind']) + ' m/c \n---------------\n'\
                        + str(forecast_list[2]['city']) + ' 12 hours' + '\ntemprature: ' + str(forecast_list[2]['temp']) \
                        + '\N{DEGREE SIGN}C' + '\n' + str(forecast_list[2]['description']) + get_emoji(forecast_list[2]['weather_id']) \
                        + '\nwind: ' + str(forecast_list[2]['wind']) + ' m/c \n---------------\n'\
                        + str(forecast_list[3]['city']) + ' 1 day' + '\ntemprature: ' + str(forecast_list[3]['temp']) \
                        + '\N{DEGREE SIGN}C' + '\n' + str(forecast_list[1]['description']) + get_emoji(forecast_list[3]['weather_id']) \
                        + '\nwind: ' + str(forecast_list[3]['wind']) + ' m/c \n---------------\n'
    else:
        answer_string = 'Sorry! No available data.'

    return answer_string


def get_usd():
    PB_URL = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
    r = requests.get(PB_URL).json()
    buy = round(float(r[0]['buy']), 2)
    sell = round(float(r[0]['sale']), 2)
    answer_string = 'usd/uah: buy: ' + str(buy) + ' sell: ' + str(sell)

    return answer_string


def get_uku_html():
    UKU_URL = 'https://ucu.edu.ua/events/'
    r = requests.get(UKU_URL)
    return r.text


def get_uku_data():
    soup = BeautifulSoup(get_uku_html(), 'lxml')
    events = reversed(soup.find_all('div', class_='event')[0:8])
    events_list =[]
    for event in events:
        date = event.find('a').text.strip()
        name = event.find('h4').text.strip()
        href = event.find('h4').find('a').get('href')
        start = event.find('p').text.strip()
        data = {
            'date': date,
            'start': start,
            'name': name,
            'href': href
        }
        answer_string = '\n' + data['date'] + '\n' + data['start'] + '\n' + data['name']  + '\n' + data['href']  + '\n'
        events_list.append(answer_string)
    answer_string = str('UKU Events\n***************') + '\n---------------\n'.join(events_list) + '\n---------------\n'

    return answer_string


def get_work_html():
    WORK_URL = 'https://www.work.ua/jobs-lviv-design-art/'
    r = requests.get(WORK_URL)
    return r.text


def get_work_data():
    soup = BeautifulSoup(get_work_html(), 'lxml')
    events_hot = soup.find('div', id='pjax-job-list').find_all('div', class_='card card-hover card-visited wordwrap job-link js-hot-block')
    events = soup.find('div', id='pjax-job-list').find_all('div', class_='card card-hover card-visited wordwrap job-link')

    events_list =[]

    for event in events_hot:
        name = event.find('h2', class_="add-bottom-sm").find('a').text.strip()
        salary = event.find('h2', class_="add-bottom-sm").find('a').text.strip()
        data = {
            'name': name,
        }
        answer_string = '\n' + data['name']
        events_list.append(answer_string)

    for event in events:
        name = event.find('h2', class_="add-bottom-sm").find('a').text.strip()
        data = {
            'name': name,
        }
        answer_string = '\n' + data['name']
        events_list.append(answer_string)

    answer_string = str('Work.ua "Дизайн, творчість"\n***************') + ''.join(events_list) + '\n---------------\n'
    print(answer_string)
    return answer_string


def get_rabota_html():
    WORK_URL = 'https://rabota.ua/jobsearch/vacancy_list?keyWords=&regionId=2&rubricIds=338&parentId=32'
    r = requests.get(WORK_URL)
    return r.text


def get_rabota_data():
    soup = BeautifulSoup(get_rabota_html(), 'lxml')
    trs = soup.find('table', class_='f-vacancylist-tablewrap')
    events_list = []
    for tr in trs:
        tds = tr.find_all('td')
        name = tds[0].find('h3').text.rstrip()
        salary = tds[0].find('div', class_='f-vacancylist-characs-block fd-f-left-middle').find('p',
                                                                                                class_='fd-beefy-soldier -price')
        if salary:
            salary = salary.text.rstrip()
        else:
            salary = ''
        answer_string = '\n' + name + '\t' + salary
        events_list.append(answer_string)

    answer_string = str('Rabota.ua "Типография, издательство"\n***************') + ''.join(
        events_list) + '\n---------------\n'

    return answer_string


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        chat_id = r['message']['chat']['id']
        user_message = r['message']['text']

        if 'weather' in user_message:
            send_message(chat_id, get_weather_now())
        elif 'forecast' in user_message:
            send_message(chat_id, get_weather_forecast())
        elif 'usd' in user_message:
            send_message(chat_id, get_usd())
        elif 'uku' in user_message:
            send_message(chat_id, get_uku_data())
        elif 'work' in user_message:
            send_message(chat_id, get_work_data())
        elif 'rabota' in user_message:
            send_message(chat_id, get_rabota_data())

        return jsonify(r)
    return 'No data available yet!!!'


def main():
    # r = get_updates()
    # chat_id = r['result'][-1]['message']['chat']['id']
    # send_message(chat_id)
    pass


if __name__ == '__main__':
    app.run()
