import requests
from bs4 import BeautifulSoup


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

