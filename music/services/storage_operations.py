import dropbox
from django.conf import settings
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.credentials import Credentials
import os

# Dropbox configurations
DROPBOX_ACCESS_TOKEN = 'YOUR_DROPBOX_ACCESS_TOKEN'

# Google Drive configurations
SCOPES = ['https://www.googleapis.com/auth/drive']
GOOGLE_DRIVE_CREDENTIALS_FILE = 'credentials.json'  # Update with your credentials file


class CloudStorageService:
    def __init__(self, storage_type):
        self.storage_type = storage_type
        self.access_token = settings.DROPBOX_ACCESS_TOKEN if storage_type == 'dropbox' else None
        self.dbx = dropbox.Dropbox(self.access_token) if storage_type == 'dropbox' else None
        self.service = None

        if storage_type == 'drive':
            creds = None
            if os.path.exists('token.json'):
                creds = Credentials.from_authorized_user_file('token.json')
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        GOOGLE_DRIVE_CREDENTIALS_FILE, SCOPES)
                    creds = flow.run_local_server(port=0)
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())
            self.service = build('drive', 'v3', credentials=creds)

    def upload_file(self, file_path, file_name, destination_path=None):
        if self.storage_type == 'dropbox':
            with open(file_path, 'rb') as f:
                self.dbx.files_upload(f.read(), destination_path or '/' + file_name)
        elif self.storage_type == 'drive':
            file_metadata = {'name': file_name}
            if destination_path:
                file_metadata['parents'] = [destination_path]
            media = {'mimeType': 'application/octet-stream', 'body': open(file_path, 'rb')}
            self.service.files().create(body=file_metadata, media_body=media).execute()


def list_files_from_google_drive():
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('drive', 'v3', credentials=creds)
    results = service.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(f"{item['name']} ({item['id']})")

