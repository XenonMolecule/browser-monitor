from __future__ import print_function
import pickle
import json
import os.path
import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.file']
MONTHS = ["January", "February", "March", "April", "May", "June", "July",
            "August", "September", "October", "November", "December"]

class RemoteLogger(object):
    def __init__(self):
        super().__init__()
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_id.json', SCOPES)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.sheets_service = build('sheets', 'v4', credentials=creds)
        self.drive_service = build('drive', 'v3', credentials=creds)
        now = datetime.datetime.now()
        self.getFile(now)

    def googleCreateFile(self, name, mimeType, parentID):
        file_metadata = {
            'name': name,
            'mimeType': mimeType,
            'parents': [parentID]
        }
        file = self.drive_service.files().create(body=file_metadata,
                                            fields='id').execute()
        return file

    def getFile(self, date):
        data = {}
        file_id = ""
        yr_str = str(date.year)
        mon_str = MONTHS[date.month-1]
        day_str = str(date.day)

        # Get the id out of the json file
        with open("files.json") as file_tree:
            data = json.load(file_tree)
            # If the year folder doesn't exist then create that folder
            if(not yr_str in data["parent"]["years"]):
                id = self.googleCreateFile(yr_str, 'application/vnd.google-apps.folder',
                                                data["parent"]["id"]).get("id")
                data["parent"]["years"][yr_str] = {}
                data["parent"]["years"][yr_str]["id"] = id
                data["parent"]["years"][yr_str]["months"] = {}
            # If the month folder doesn't exist then create that folder
            if(not mon_str in data["parent"]["years"][yr_str]["months"]):
                id = self.googleCreateFile(mon_str, 'application/vnd.google-apps.folder',
                                data["parent"]["years"][yr_str]["id"]).get("id")
                data["parent"]["years"][yr_str]["months"][mon_str] = {}
                data["parent"]["years"][yr_str]["months"][mon_str]["id"] = id
                data["parent"]["years"][yr_str]["months"][mon_str]["days"] = {}
            # If the day file doesn't exist then create that file
            if(not day_str in data["parent"]["years"][yr_str]["months"][mon_str]["days"]):
                file_id = self.googleCreateFile(str(date.month) + "/" + day_str + "/" + yr_str,
                        'application/vnd.google-apps.spreadsheet',
                        data["parent"]["years"][yr_str]["months"][mon_str]["id"]).get("id")
                data["parent"]["years"][yr_str]["months"][mon_str]["days"][day_str] = file_id
            else:
                file_id = data["parent"]["years"][yr_str]["months"][mon_str]["days"][day_str]

        with open("files.json", "w") as file_tree:
            # Update file_tree
            json.dump(data, file_tree, indent=4)

        return file_id
