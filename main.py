import requests
import json
import sqlite3
from google_cal import insert_events
import sys
import re

URL = 'https://gb.ru/login'
SCHEDULE_URL = 'https://gb.ru/api/v2/schedule'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}


def get_cred():
    login = input('Введите логин с сайта GB: ').strip()
    while not re.search(r"^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*", login, re.IGNORECASE):
        login = input('То, что вы ввели, не похоже на email. Попробуйте ещё раз: ').strip()
    password = input('Введите пароль с сайта GB: ')
    data = {
    'user[email]': login,
    'user[password]': password
    }
    return data


def get_session(url, headers, data):
    session = requests.Session()
    response = session.post(url, data=data, headers=headers)
    return session


def get_json(session, url, headers):
    schedule = session.get(url, headers=headers)
    return schedule.text


def get_lessons(data):
    try:
        data_dict = json.loads(data)
        lessons = data_dict['lessons']
        table = []
        url = 'https://gb.ru'
        themes = get_themes(data_dict)
        for lesson in lessons:
            if lesson['stream_id'] in themes:
                table.append([lesson['id'], lesson['datetime'], lesson['title'], url+lesson['link'], lesson['stream_id']])
        return table
    except KeyError:
        print('''Ошибка доступа к данным. 
Проверьте правильность логина и пароля и попробуйте перезапустить программу.''')
        sys.exit()


def get_themes(data_dict):
    themes_list = data_dict['streams']
    themes = []
    for theme in themes_list:
        if get_reply(theme['title']):
            themes.append(theme['id'])
    return themes
    

def get_reply(theme):
    choice = ''
    while choice not in ('да', 'нет'):
        choice = input(f'Добавить в календарь мероприятия по теме "{theme}"? (да/нет): ').lower()
    return choice == 'да'


def write_db(sheet):
    db = sqlite3.connect('cal.db')
    cur = db.cursor()
    db.execute('CREATE TABLE IF NOT EXISTS {}(id PRIMARY KEY, datetime, title, link, stream_id)'.format('calendar'))
    db.commit()
    for value in sheet:
        if not cur.execute('SELECT EXISTS(SELECT id FROM calendar WHERE id = {})'.format(value[0])).fetchone()[0]:
            cur.execute('INSERT INTO calendar VALUES(?, ?, ?, ?, ?)', (value[0], value[1], value[2], value[3], value[4]))
            db.commit()
            insert_events(value)
    db.close()


def main():
    data = get_cred()
    session = get_session(URL, HEADERS, data)
    json_dict = get_json(session, SCHEDULE_URL, HEADERS)
    table = get_lessons(json_dict)
    write_db(table)









if __name__ == "__main__":
    main()
