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
        self.date = datetime.datetime.strptime(date + " 2023", "%B %d %Y")
        self.platform = platform
        self.content = content
        self.c2a = c2a
        self.tags = tags


tasks = []
for row in rows:
    print(row)
    tasks.append(Task(row[0], row[1], row[2], row[3], row[4]))

# for every task in tasks create a google calendar event
SCOPES = ["https://www.googleapis.com/auth/calendar"]

creds = None

# check if token exists
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)


try:
    service = build("calendar", "v3", credentials=creds)

    # Create test calendar
    calendar = {
        "summary": "Test Calendar",
    }

    created_calendar = service.calendars().insert(body=calendar).execute()

    print("Created calendar: ", created_calendar["id"])


except HttpError as error:
    print("An error occured: %s", error)
