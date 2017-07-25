from django.test import TestCase
from api.models import Take, Language, Book, User, Comment, Chunk, Project, Chapter
from rest_framework.test import APIClient
from rest_framework import status
import os
from sys import platform
import os.path

view_url = 'http://127.0.0.1:8000/api/zip_files/'
upload_url = 'http://127.0.0.1:8000/api/upload/zip'
my_file = 'en-x-demo2_ulb_b42_mrk_c06_v01-03_t11.wav'


class ProjectZipFileViewTestCases(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.language_object = Language(slug='en-x-demo', name='english')
        self.book_object = Book(name='genesis', booknum=5, slug='gen')
        self.project_object = Project(version='ulb', mode='chunk',
                                      anthology='nt', is_source=False, language = self.language_object, book = self.book_object)
        self.chapter_object = Chapter(number=1, checked_level=1, is_publish=False, project = self.project_object)
        self.chunk_object = Chunk(startv=0, endv=3, chapter = self.chapter_object)
        self.user_object = User(name='testy', agreed=True, picture='mypic.jpg')
        self.take_object = Take(location=my_file, is_publish=True,
                                duration=0, markers=True, rating=2, chunk = self.chunk_object, user = self.user_object)
        self.comment_object = Comment(location='/test-location/',
                                      content_object = self.take_object, user = self.user_object)

    def test_post_request_for_project_zip_file_view(self):
        """POST request for Project Zip File view expects a wav file as input, and will return a zip file"""
        self.language_object.save()
        self.book_object.save()
        self.project_object.save()
        self.chapter_object.save()
        self.chunk_object.save()
        self.user_object.save()
        self.take_object.save()
        old_folder_size = len(os.listdir('media/export'))  # find the total number of files in the media/export folder
        self.response = self.client.post(view_url, {'language': 'en-x-demo', 'version': 'ulb', 'book': 'gen'}, format='json')
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)  # making sure that we return the correct status code
        new_folder_size = len(os.listdir('media/export'))  # new zip file should have been added to media/export folder
        self.assertNotEqual(old_folder_size, new_folder_size)  # check that a new file exists in media/export
        self.take_object.delete()
        self.user_object.delete()
        self.book_object.delete()

    def test_posting_file_to_api_returns_success_response(self):
        """Testing That zip files can be uploaded to the api"""
        with open('en-x-demo2_ulb_mrk.zip', 'rb') as test_zip:
            self.response = self.client.post(upload_url, {'Media type': '*/*', 'Content': test_zip},
                                             format='multipart')
            self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_that_we_get_403_error_when_not_enough_parameters_in_ProjectZipFile(self):
        """Testing that submitting a POST request through book key search returns an object"""
        # saving objects in temporary database so they can be read by the API
        self.response = self.client.post(view_url, {'language': 'en-x-demo', 'version': 'ulb'},
                                    format='json')  # telling the API that I want all takes that are in book English
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_that_we_get_200_when_enough_parameters_in_ProjectZipFile(self):
        """Testing that submitting a POST request through book key search returns an object"""
        # saving objects in temporary database so they can be read by the API
        self.language_object.save()
        self.book_object.save()
        self.project_object.save()
        self.chapter_object.save()
        self.chunk_object.save()
        self.user_object.save()
        self.take_object.save()
        self.response = self.client.post(view_url, {'language': 'en-x-demo', 'version': 'ulb', 'book':'gen'},
                                    format='json')  # telling the API that I want all takes that are in book English
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def tearDown(self):
        if platform == "darwin":  # OSX
            os.system('rm -rf ' + 'media/export')  # cleaning out all files generated during tests
            os.system('mkdir ' + 'media/export')
        elif platform == "win32":  # Windows
            os.system('rmdir /s /q ' + 'media\export')  # cleaning out all files generated during tests
            os.system('mkdir ' + 'media\export')
