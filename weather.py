import requests
import json


def write_json(data, filename='weather.json'):
    with open(filename, 'w', encoding='utf-8', errors='ignore') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


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
    icon = r['weather'][0]['icon']
    temp = r['main']['temp']
    wind = r['wind']['speed']

    if cod == 200:
        answer_string = str(city) + ' now' + '\ntemprature: ' + str(temp) + '\N{DEGREE SIGN}C' + '\n' + str(
            description) + get_emoji(weather_id) + '\nwind: ' + str(wind) + ' m/c \n'
    else:
        answer_string = 'Sorry! No available data.'


    return answer_string
