import dropbox
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


def upload_to_dropbox(file_path, destination_path):
    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    with open(file_path, 'rb') as f:
        dbx.files_upload(f.read(), destination_path)


def upload_to_google_drive(file_path, file_name, folder_id=None):
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

    service = build('drive', 'v3', credentials=creds)

    file_metadata = {'name': file_name}
    if folder_id:
        file_metadata['parents'] = [folder_id]

    media = {'mimeType': 'application/octet-stream', 'body': open(file_path, 'rb')}
    service.files().create(body=file_metadata, media_body=media).execute()


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


# Example usage
if __name__ == "__main__":
    # Uploading to Dropbox
    upload_to_dropbox('local_file_path.txt', '/destination_path/filename.txt')

    # Uploading to Google Drive
    upload_to_google_drive('local_file_path.txt', 'filename.txt')

    # Listing files from Google Drive
    list_files_from_google_drive()
