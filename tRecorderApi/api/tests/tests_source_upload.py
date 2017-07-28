from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Take, Language, Book, Project,Chapter,Chunk,User,Comment
import os
from sys import platform
from django.conf import settings

my_file = 'media/dump'
base_url = 'http://127.0.0.1:8000/api/'
location_wav = settings.BASE_DIR + 'en-x-demo2_ulb_b42_mrk_c06_v01-03_t11.wav'


class SourceFileUploadViewTestCases(TestCase):

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
        self.take = Take.objects.create(location=location_wav, is_publish=True,
                                   duration=0, markers="{\"test\" : \"true\"}", rating=2, chunk=self.chunk, user=self.user)
        self.comment_object = Comment.objects.create(location='/test-location/',
                                      content_object=self.take, user=self.user)

    # def test_that_uploading_source_tr_file_with_wav_file_returns_200_OK(self):
    #     with open(settings.BASE_DIR + '/en-x-demo2_ulb.tr', 'rb') as test_tr:
    #         self.response = self.client.post(base_url + 'source/en-x-demo2_ulb.tr',
    #                                          {'upload': test_tr,'Media type': '*/*', 'Content': test_tr}, format='multipart')
    #         self.assertEqual(self.response.status_code, status.HTTP_200_OK)
    #
    # def test_that_we_get_400_error_when_not_enough_parameters_are_uploaded_in_SourceFile(self):
    #     """Testing that submitting a POST request through book key search returns an object"""
    #     # saving objects in temporary database so they can be read by the API
    #     self.response = self.client.post(base_url + 'get_source/', {'book': 'book', 'book': 'book'},
    #                                 format='json')  # telling the API that I want all takes that are in book English
    #     self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)
    #     # freeing up the temporary database
    #
    # def test_that_we_get_400_error_when_no_source_is_uploaded_in_SourceFile(self):
    #     """Testing that submitting a POST request through book key search returns an object"""
    #     # saving objects in temporary database so they can be read by the API
    #     self.response = self.client.post(base_url + 'get_source/', {'language': 'eng', 'version': 'ulb'},
    #                                 format='json')  # telling the API that I want all takes that are in book English
    #     self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

    def tearDown(self):
        if platform == "darwin": #OSX
            pass
            # os.system('rm -rf ' + settings.BASE_DIR + '/' + my_file)  # cleaning out all files generated during tests
            # os.system('mkdir ' + settings.BASE_DIR + '/' + my_file)
        elif platform == "win32": #Windows
            pass
            # os.system('rmdir /s /q ' + 'media\dump')  # cleaning out all files generated during tests
            # os.system('mkdir ' + 'media\dump')
        self.take.delete()
        self.user.delete()
        self.chunk.delete()
        self.chap.delete()
        self.proj.delete()
        self.book.delete()
        self.lang.delete()