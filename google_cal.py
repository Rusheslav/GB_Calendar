from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from datetime import datetime, timedelta


def insert_events(data):
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    store = file.Storage('storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)

    CAL = build('calendar', 'v3', http=creds.authorize(Http()))
    
    title = data[2]
    start = data[1]
    d = datetime.strptime(start.split('+')[0], '%Y-%m-%dT%H:%M:%S.%f')
    dt = str(d + timedelta(hours=2))
    end = dt.replace(' ', 'T') + '+' + start.split('+')[1]
    event = {
        'summary': title,
        'start': {'dateTime': start},
        'end': {'dateTime': end}
    }


    e = CAL.events().insert(calendarId='primary',
        sendNotifications=True, body=event).execute()

    print('''*** %r event added:
        Start: %s
        End: %s'''% (e['summary'], e['start']['dateTime'], e['end']['dateTime']))
