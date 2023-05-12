import csv
import datetime

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# open csv file
rows = []
with open("may_tasks.csv", "r") as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    for row in csvreader:
        rows.append(row)
        for row in csvreader:
            rows.append(row)


# get the columns
class Task:
    def __init__(self, date, platform, content, c2a, tags):
        start = date + ' 2023 19:30:00'
        end = date + ' 2023 20:30:00'
        self.start = datetime.datetime.strptime(
            start, "%B %d %Y %H:%M:%S")
        self.platform = platform
        self.content = content
        self.c2a = c2a
        self.tags = tags
        self.end = datetime.datetime.strptime(
            end, "%B %d %Y %H:%M:%S")


tasks = []
for row in rows:
    tasks.append(Task(row[0], row[1], row[2], row[3], row[4]))

# for every task in tasks create a google calendar event
SCOPES = ["https://www.googleapis.com/auth/calendar"]

creds = None

# check if token exists
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

try:
    service = build("calendar", "v3", credentials=creds)

    test_calendar_id = 'faa004c9827e157ad276425b0c63bff3a2fdcb8e9a52050df77fc090374d21b2@group.calendar.google.com'
    band_calendar_id = '67934ed0386dc05e51b0d575dbe787ece3c7d518916a44af41475d6683dffe41@group.calendar.google.com'

    # band_calendar = service.calendars().get(calendarId=band_calendar_id).execute()

    # for every task create an event in the Test Calendar
    events = []
    for task in tasks:
        description = "Content: {}\nCall to Action:{}\nTags:{}".format(
            task.content, task.c2a, task.tags)
        print(description)
        print('\n')
        event = {
            'summary': task.platform,
            'description': description,
            'start': {
                'dateTime': task.start.strftime('%Y-%m-%dT%H:%M:%S-04:00')
            },
            'end': {
                'dateTime': task.start.strftime('%Y-%m-%dT%H:%M:%S-04:00')
            }
        }
        event = service.events().insert(calendarId=band_calendar_id, body=event).execute()
        events.append(event)
except HttpError as error:
    print("An error occured: %s", error)
