import requests
import json


def write_json(data, filename='forecast.json'):
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
    print(answer_string)

    return answer_string

