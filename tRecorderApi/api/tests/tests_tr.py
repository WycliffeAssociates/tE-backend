from django.test import TestCase
from rest_framework.test import APIClient
import os
from api.models import *
from sys import platform

base_url = 'http://127.0.0.1:8000/api/'
tr_path = 'media/temp/'
tr_filepath = 'en-x-demo2_ulb.tr'

class TRTestCases(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.take_object = Take(location=tr_filepath, is_publish=False, duration=0, markers=True, rating=2)
        self.language_object = Language(slug='en-x-demo', name='english')
        self.book_object = Book(name='english', booknum=5, slug='slug')
        self.user_object = User(name='testy', agreed=True, picture='mypic.jpg')
        self.comment_object = Comment(location='/test-location/', content_type_id = 1, object_id = 1 )
        self.chunk_object = Chunk(startv=0, endv=3)
        self.project_object = Project(is_source=False, is_publish=False, version='ulb', anthology='nt')
        self.chapter_object = Chapter(number=1, checked_level=1, is_publish=False)

    def test_that_tR_file_was_returned_in_response_from_wav_files(self):
        """Verify that files are ready for exporting in a folder with file extension tR only"""
        self.take_object.save()
        self.language_object.save()
        # from SourceFileView class
        # upload zip maybe?
        self.client.post(base_url + 'upload/zip', {'Media type': '*/*', 'Content': 'en-x-demo2_ulb_mrk.zip'})
        self.response = self.client.post(base_url + 'get_source', {'language': 'en-x-demo', 'version': 'ESV', 'book': 'en'},
                                         format='json')
        # just checking for existence of .tr file extension
        self.assertIn('en-x-demo2_ulb.tr', os.listdir(tr_path))
        self.take_object.delete()
        self.language_object.delete()

    def test_that_tR_is_in_correct_directory(self):
        """Verify that tR was created in correct directory"""
        self.book_object.save()
        self.user_object.save()
        self.comment_object.save()
        self.language_object.save()
        self.take_object.save()
        self.response = self.client.post(base_url + 'get_source/', {'language': 'en-x-demo', 'version': 'ESV', 'book': 'en'},
                                         format='json')
        # double check tr_path variable
        self.assertTrue(os.path.exists(tr_path))
        self.take_object.delete()
        self.language_object.delete()
        self.book_object.delete()
        self.user_object.delete()
        self.comment_object.delete()

    def tearDown(self):
         if platform == "darwin":  # OSX
             os.system('rm -rf ' + 'media/tmp')  # cleaning out all files generated during tests
             os.system('mkdir ' + 'media/tmp')
         elif platform == "win32":  # Windows
             os.system('rmdir /s /q ' + "media" + "\\t" +"emp")  # cleaning out all files generated during tests
             os.system('mkdir ' + "media" + "\\t" +"emp")