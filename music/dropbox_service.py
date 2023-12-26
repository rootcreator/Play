import dropbox
from django.conf import settings


class DropboxService:
    def __init__(self):
        self.access_token = settings.DROPBOX_ACCESS_TOKEN
        self.dbx = dropbox.Dropbox(self.access_token)

    def upload_file(self, file_path, file):
        with open(file_path, 'rb') as f:
            self.dbx.files_upload(f.read(), file)

    def get_shared_link(self, file_path):
        shared_link_settings = dropbox.sharing.SharedLinkSettings(
            requested_visibility=dropbox.sharing.RequestedVisibility.public)
        shared_link = self.dbx.sharing_create_shared_link_with_settings(file_path, settings=shared_link_settings)
        return shared_link.url
