from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
import os

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

#    def test_upload_non_wav_file_returns_403_error(self):
#         """Verify that uploading a zip file containing non .wav files returns 403 FORBIDDEN code"""
#         with open('no_wav_files.zip', 'rb') as test_zip_nowav:
#              self.response = self.client.post(base_url + 'upload/zip', {'Media type' : '*/*', 'Content' : test_zip_nowav}, format='multipart')
#              self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)#

#    def tearDown(self):
#        os.system('rm -rf ' + my_file)  # cleaning out all files generated during tests
#        os.system('mkdir ' + my_file)#
#
#
#
#
#
#
#

    def test_upload_non_wav_file_returns_403_error(self):
         """Verify that uploading a zip file containing non .wav files returns 403 FORBIDDEN code"""
         with open('no_wav_files.zip', 'rb') as test_zip_nowav:
              self.response = self.client.post(base_url + 'upload/zip', {'Media type' : '*/*', 'Content' : test_zip_nowav}, format='multipart')
              self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)

    def tearDown(self):
        os.system('rm -rf ' + my_file)  # cleaning out all files generated during tests
        os.system('mkdir ' + my_file)