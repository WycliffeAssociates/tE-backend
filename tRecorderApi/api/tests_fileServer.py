from django.test import TestCase
from datetime import datetime
from models import Take, Language, Book, User, Comment
from views_sets import SourceFileView,FileUploadView, FileStreamView
from rest_framework.test import APIClient
from rest_framework import status
import os
from sys import platform
import hashlib

##Creating a text file to log the results of each of the tests
#base_url = 'http://127.0.0.1:8000/api/'
#my_file = 'media/dump'#
#

base_url = 'http://127.0.0.1:8000/api/'
my_file = 'media/dump'
tr_path = 'media/tmp/english_ulb.tr'


class FileServerTests(TestCase):
    def SetUp(self):
        """Set up environment for fileServer test suite"""
        self.client = APIClient()
        self.take_data = {'location' : 'my_file', 'chapter' : 5, 'is_export' : True, 'is_source' : False}
        self.lang_data = {'lang' : 'english', 'code' : 'abc'}
        self.user_data = {'name' : 'tester', 'agreed' : True, 'picture' : 'test.pic'}
        self.comment = {'location':'my_file'}
        self.book_data = {'code':'ex', 'name' : 'english', 'booknum' : 5}
        self.take_object = Take(location='my_file', chapter=5, is_export=True, is_source=False, id=1, language_id=1, book_id=1, user_id=1)
        self.language_object = Language(slug='en-x-demo', name='english', id=1)
        self.book_object = Book(name='english', booknum=5, id=1)
        self.user_object = User(name='testy', agreed=True, picture='mypic.jpg', id=1)
        self.comment_object = Comment(location='/test-location/', id=1)

    def test_that_uploading_non_zip_file_returns_403_error(self):
         """Verify that uploading a non zip file will return a 403 FORBIDDEN code"""
         with open('Sample.docx', 'rb') as test_nonzip:
              self.response = self.client.post(base_url + 'upload/zip', {'Media type' : '*/*', 'Content' : test_nonzip}, format='multipart')
              self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)

    def test_that_uploading_empty_wav_file_returns_403_error(self):
        """Verify that uploading a zip file containing non .wav files returns 403 FORBIDDEN code"""
        with open('empty_zip_folder.zip', 'rb') as test_zip_nowav:
            self.response = self.client.post(base_url + 'upload/zip', {'Media type' : '*/*', 'Content' : test_zip_nowav}, format='multipart')
            self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)

    def test_that_uploading_non_wav_file_returns_403_error(self):
        """Verify that uploading a zip file containing non .wav files returns 403 FORBIDDEN code"""
        with open('no_wav_files.zip', 'rb') as test_zip_nowav:
            self.response = self.client.post(base_url + 'upload/zip', {'Media type' : '*/*', 'Content' : test_zip_nowav}, format='multipart')
            self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)

    def tearDown(self):
        if platform == "darwin": #OSX
            os.system('rm -rf ' + my_file)  # cleaning out all files generated during tests
            os.system('mkdir ' + my_file)
        elif platform == "win32": #Windows
            os.system('rmdir /s /q ' + 'media\dump')  # cleaning out all files generated during tests
            os.system('mkdir ' + 'media\dump')









