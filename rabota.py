import requests
from bs4 import BeautifulSoup


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
        salary = tds[0].find('div', class_='f-vacancylist-characs-block fd-f-left-middle').find('p', class_='fd-beefy-soldier -price')
        if salary:
            salary = salary.text.rstrip()
        else:
            salary = ''
        answer_string = '\n' + name + '\t' + salary
        events_list.append(answer_string)

    answer_string = str('Rabota.ua "Типография, издательство"\n***************') + ''.join(events_list) + '\n---------------\n'

    return answer_string

