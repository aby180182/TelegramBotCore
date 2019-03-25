import requests
from bs4 import BeautifulSoup


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

    return answer_string

