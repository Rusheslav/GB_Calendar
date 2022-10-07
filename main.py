import requests
from config import login, password
import json
from tabulate import tabulate

URL = 'https://gb.ru/login'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}

DATA = {
    'user[email]': login,
    'user[password]': password
}

SCHEDULE_URL = 'https://gb.ru/api/v2/schedule'


def get_session(url, headers, data):
    session = requests.Session()
    response = session.post(url, data=data, headers=headers)
    return session


def get_html(session, url, headers):
    schedule = session.get(url, headers=headers)
    return schedule.text


def get_lessons(data):
    data_dict = json.loads(data)
    lessons = data_dict['lessons']
    table = [['Дата', 'Время', 'Занятие', 'Ссылка']]
    url = 'https://gb.ru'
    for lesson in lessons:
        if lesson['stream_id'] not in [45377, 45755, 45763]:   
            table.append([lesson['datetime'].split('T')[0], lesson['datetime'].split('T')[1].split(':')[0]+':00', lesson['title'], url+lesson['link']])
    return table


def main():
    session = get_session(URL, HEADERS, DATA)
    data = get_html(session, SCHEDULE_URL, HEADERS)
    table = get_lessons(data)
    print(tabulate(table))









if __name__ == "__main__":
    main()
