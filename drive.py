from __future__ import print_function
import os.path
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

class drive:
    def __init__(self,creds):
        self.SERVICE = build('drive','v3',credentials=creds)

    def __get_file_info(self,file_id):
        return self.SERVICE.files().get(fileId=file_id).execute()

    def download_file(self,file_id,file_name):
        file_info = self.__get_file_info(file_id)
        if not file_name.strip():
            file_name = file_info['name']

        request = self.SERVICE.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request=request)
        done = False

        while not done:
            status, done = downloader.next_chunk()
            print('Download %d%%.' % int(status.progress() * 100))

        with open(file_name, 'wb') as f:
            fh.seek(0)
            f.write(fh.read())
            f.close()
        