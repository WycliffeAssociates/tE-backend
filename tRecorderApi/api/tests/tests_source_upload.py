from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Take, Language, Book, Project,Chapter,Chunk,User,Comment
import os
from sys import platform

my_file = 'media/dump'
base_url = 'http://127.0.0.1:8000/api/'


class SourceFileUploadViewTestCases(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.language_object = Language(slug='en-x-demo', name='english')
        self.book_object = Book(name='mark', booknum=5, slug='mrk')
        self.project_object = Project(version='ulb', mode='chunk',
                                      anthology='nt', is_source=False, language=self.language_object,
                                      book=self.book_object)
        self.chapter_object = Chapter(number=1, checked_level=1, is_publish=False, project=self.project_object)
        self.chunk_object = Chunk(startv=0, endv=3, chapter=self.chapter_object)
        self.user_object = User(name='testy', agreed=True, picture='mypic.jpg')
        self.take_object = Take(location=my_file, is_publish=True,
                                duration=0, markers=True, rating=2, chunk=self.chunk_object, user=self.user_object)
        self.comment_object = Comment(location='/test-location/',
                                      content_object=self.take_object, user=self.user_object)

    #throws error
    def test_that_uploading_source_tr_file_with_wav_file_returns_200_OK(self):
        with open('en-x-demo2_ulb.tr', 'rb') as test_tr:
            self.response = self.client.post(base_url + 'source/en-x-demo2_ulb.tr',
                                             {'Media type': '*/*', 'Content': test_tr}, format='multipart')
            self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_that_we_get_400_error_when_not_enough_parameters_are_uploaded_in_SourceFile(self):
        """Testing that submitting a POST request through book key search returns an object"""
        # saving objects in temporary database so they can be read by the API
        self.response = self.client.post(base_url + 'get_source/', {'book': 'book', 'book': 'book'},
                                    format='json')  # telling the API that I want all takes that are in book English
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)
        # freeing up the temporary database

    def test_that_we_get_400_error_when_no_source_is_uploaded_in_SourceFile(self):
        """Testing that submitting a POST request through book key search returns an object"""
        # saving objects in temporary database so they can be read by the API
        self.response = self.client.post(base_url + 'get_source/', {'language': 'eng', 'version': 'ulb'},
                                    format='json')  # telling the API that I want all takes that are in book English
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

    def tearDown(self):
        if platform == "darwin": #OSX
            os.system('rm -rf ' + my_file)  # cleaning out all files generated during tests
            os.system('mkdir ' + my_file)
        elif platform == "win32": #Windows
            os.system('rmdir /s /q ' + 'media\dump')  # cleaning out all files generated during tests
            os.system('mkdir ' + 'media\dump')