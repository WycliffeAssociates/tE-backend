from django.test import TestCase
from api.models import Take, Language, Book, User, Comment, Chunk, Project, Chapter
from rest_framework.test import APIClient
from rest_framework import status
import os
from sys import platform
import os.path
from django.conf import settings

view_url = 'http://127.0.0.1:8000/api/zip_files/'
base_url = 'http://127.0.0.1:8000/api/'
upload_url = 'http://127.0.0.1:8000/api/upload/zip'
my_file = settings.BASE_DIR + '/en-x-demo2_ulb_b42_mrk_c06_v01-03_t11.wav'


class ProjectZipFileViewTestCases(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.lang = Language.objects.create(slug='en-x-demo', name='english')
        self.book = Book.objects.create(name='mark', booknum=5, slug='mrk')
        self.proj = Project.objects.create(version='ulb', mode='chunk',
                                           anthology='nt', is_source=False, language=self.lang,
                                           book=self.book)
        self.chap = Chapter.objects.create(number=1, checked_level=1, is_publish=False, project=self.proj)
        self.chunk = Chunk.objects.create(startv=0, endv=3, chapter=self.chap)
        self.user = User.objects.create(name='testy', agreed=True, picture='mypic.jpg')
        self.take = Take.objects.create(location=my_file, is_publish=True,
                                        duration=0, markers="{\"test\" : \"true\"}", rating=2, chunk=self.chunk,
                                        user=self.user)
        self.comment_object = Comment.objects.create(location='/test-location/',
                                      content_object=self.take, user=self.user)
        self.take_data = {
            "id": 789878987,
            "location": "my_file",
            "duration": 3,
            "rating": 3,
            "is_publish": True,
            "markers": "marked",
            "date_modified": "2017-07-26T12:29:02.828000Z"}

    #throws error
    def test_post_request_for_project_zip_file_view(self):
        """POST request for Project Zip File view expects a wav file as input, and will return a zip file"""

        old_folder_size = len(os.listdir('media/export'))  # find the total number of files in the media/export folder
        self.response = self.client.post(view_url, {"language": "en-x-demo2","version": "ulb", "book":"mrk"}, format='json')
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)  # making sure that we return the correct status code
        new_folder_size = len(os.listdir('media/export'))  # new zip file should have been added to media/export folder
        self.assertNotEqual(old_folder_size, new_folder_size)  # check that a new file exists in media/export

    def test_posting_file_to_api_returns_success_response(self):
        """Testing That zip files can be uploaded to the api"""
        with open(settings.BASE_DIR + '/en-x-demo2_ulb_mrk.zip', 'rb') as test_zip:
            self.response = self.client.post(upload_url, {'Media type': '*/*', 'Content': test_zip},
                                             format='multipart')
            self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_that_we_get_403_error_when_not_enough_parameters_in_ProjectZipFile(self):
        """Testing that submitting a POST request through book key search returns an object"""
        # saving objects in temporary database so they can be read by the API
        self.response = self.client.post(view_url, {'language': 'en-x-demo', 'version': 'ulb'},
                                    format='json')  # telling the API that I want all takes that are in book English
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_that_we_get_400_when_enough_parameters_but_no_takes_in_ProjectZipFile(self):
        """Testing that submitting a POST request through book key search returns an object"""
        # saving objects in temporary database so they can be read by the API

        self.response = self.client.post(view_url, {'language': 'en-x-demo', 'version': 'ulb', 'book':'gen'},
                                    format='json')  # telling the API that I want all takes that are in book English
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

    #throws error, can't see takes for some reason
    def test_that_we_get_200_when_enough_parameters_and_takes_in_ProjectZipFile(self):
        """Testing that submitting a POST request will return a project zip file"""
        # saving objects in temporary database so they can be read by the API

        self.client.post(base_url + 'takes/', self.take_data, format='json')
        self.response = self.client.post(view_url, {'language': 'en-x-demo', 'version': 'ulb', 'book': 'gen'},
                                         format='json')  # telling the API that I want all takes that are in book English
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)


    def tearDown(self):
        if platform == "darwin":  # OSX
            os.system('rm -rf ' + 'media/export')  # cleaning out all files generated during tests
            os.system('mkdir ' + 'media/export')
        elif platform == "win32":  # Windows
            os.system('rmdir /s /q ' + 'media\export')  # cleaning out all files generated during tests
            os.system('mkdir ' + 'media\export')
        self.take.delete()
        self.user.delete()
        self.chunk.delete()
        self.chap.delete()
        self.proj.delete()
        self.book.delete()
        self.lang.delete()
        self.comment_object.delete()