from django.test import TestCase
from rest_framework.test import APIClient
import os
from api.models import *
from sys import platform
from django.conf import settings
import time

base_url = 'http://127.0.0.1:8000/api/'
tr_path = settings.BASE_DIR + '/media/tmp'
tr_filepath = settings.BASE_DIR + '/en-x-demo2_ulb.tr'
location_wav = 'en-x-demo2_ulb_b42_mrk_c06_v04-06_t08.wav'

class TRTestCases(TestCase):

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

    def test_that_tR_file_was_returned_in_response_from_wav_files(self):
        """Verify that files are ready for exporting in a folder with file extension tR only"""
        print settings.BASE_DIR
        self.client.post(base_url + 'upload/zip', {'Media type': '*/*', 'Content': 'en-x-demo2_ulb_mrk.zip'})
        self.response = self.client.post(base_url + 'get_source', {'language': 'en-x-demo', 'version': 'ulb'},
                                         format='json')
        # verify that tr file now exists
        # unexpected behavior where my assert runs before tr file is created
        # but examination of the file structure does verify that tr file is created even when test fails
        self.assertTrue(os.path.exists(tr_path + '/en-x-demo_ulb_mrk.tr'))

    def test_that_tR_is_in_correct_directory(self):
        """Verify that tR was created in correct directory"""

        self.response = self.client.post(base_url + 'get_source/', {'language': 'en-x-demo', 'version': 'ulb', 'book': 'mrk'},
                                         format='json')
        # double check tr_path variable
        self.assertTrue(os.path.exists(tr_path))

    def tearDown(self):
         if platform == "darwin":  # OSX
             pass
            #os.system('rm -rf ' + settings.BASE_DIR + '/media/tmp')  # cleaning out all files generated during tests
            #os.system('mkdir ' + settings.BASE_DIR + '/media/tmp')
         elif platform == "win32":  # Windows
             pass
             #os.system('rmdir /s /q ' + settings.BASE_DIR + "/media/tmp")  # cleaning out all files generated during tests
             #os.system('mkdir ' + settings.BASE_DIR + "/media/tmp")
         self.take.delete()
         self.user.delete()
         self.chunk.delete()
         self.chap.delete()
         self.proj.delete()
         self.book.delete()
         self.lang.delete()

