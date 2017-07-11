from django.test import TestCase
from datetime import datetime
from views import SourceFileView,FileUploadView, FileStreamView
from rest_framework.test import APIClient
from rest_framework import status
import os
from sys import platform

##Creating a text file to log the results of each of the tests
#base_url = 'http://127.0.0.1:8000/api/'
#my_file = 'media/dump'#
#

base_url = 'http://127.0.0.1:8000/api/'
my_file = 'media/dump'

class fileServerTestCases(TestCase):
    def SetUp(self):
        """Set up environment for fileServer test suite"""
        self.client = APIClient()
        self.sourcefileview_object = SourceFileView(language = 'english', version = 'ulb')

#    def test_upload_non_wav_file_returns_403_error(self):
#         """Verify that uploading a zip file containing non .wav files returns 403 FORBIDDEN code"""
#         with open('no_wav_files.zip', 'rb') as test_zip_nowav:
#              self.response = self.client.post(base_url + 'upload/zip', {'Media type' : '*/*', 'Content' : test_zip_nowav}, format='multipart')
#              self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)#

    def test_that_uploading_non_zip_file_returns_403_error(self):
         """Verify that uploading a non zip file will return a 403 FORBIDDEN code"""
         with open('Sample.docx', 'rb') as test_nonzip:
              self.response = self.client.post(base_url + 'upload/zip', {'Media type' : '*/*', 'Content' : test_nonzip}, format='multipart')
              self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)

    def test_that_uploading_non_wav_file_returns_403_error(self):
         """Verify that uploading a zip file containing non .wav files returns 403 FORBIDDEN code"""
         with open('no_wav_files.zip', 'rb') as test_zip_nowav:
              self.response = self.client.post(base_url + 'upload/zip', {'Media type' : '*/*', 'Content' : test_zip_nowav}, format='multipart')
              self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)

    ################################################################

    def test_that_tR_file_was_created_from_wav_files(self):
        """Verify that files are ready for exporting in a folder with file extension tR only"""
        self.sourcefileview_object.save()
        #save sourcefileview object to database
        response = self.client.post(base_url + 'get_source', {'language': 'english', 'version': 'ulb'})
        self.assertContains(response, '.tr')
        #or  response.endswith('tr') or convert response to a string and then check?

    def test_that_source_audio_in_tR_file_is_MP3_format(self):
        """Verify that source audio in tR file contains files with MP3 file ext. only"""
        self.sourcefileview_object.save()
        response = self.client.post(base_url + 'get_source', {'language': 'english', 'version': 'ulb'})
        #assert that media/tmp file_path_mp3 contains mp3 files

    def tearDown(self):
        if platform == "darwin": #OSX
            os.system('rm -rf ' + my_file)  # cleaning out all files generated during tests
            os.system('mkdir ' + my_file)
        elif platform == "win32": #Windows
            os.system('rmdir /s /q ' + 'media\dump')  # cleaning out all files generated during tests
            os.system('mkdir ' + 'media\dump')







