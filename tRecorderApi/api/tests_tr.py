from django.test import TestCase
from rest_framework.test import APIClient
import os
from models import *
from sys import platform

base_url = 'http://127.0.0.1:8000/api/'
tr_path = 'media/tmp/'
tr_filepath = 'en-x-demo2_ulb.tr'

class TRTestCases(TestCase):

    def setUp(self):
        """Set up environment for api view test suite"""
        self.client = APIClient()
        self.take_object = Take(location=tr_filepath, chapter=5, version='ESV', is_export=False, is_source=True, id=1,
                                language_id=1, book_id=1, user_id=1)
        self.language_object = Language(slug='en-x-demo', name='english', id=1)
        self.book_object = Book(name='Mark', slug='en', booknum=5, id=1)
        self.user_object = User(name='testy', agreed=True, picture='mypic.jpg', id=1)
        self.comment_object = Comment(location='/test-location/', id=1)

    def test_that_tR_file_was_returned_in_response_from_wav_files(self):
        """Verify that files are ready for exporting in a folder with file extension tR only"""
        self.take_object.save()
        self.language_object.save()
        # from SourceFileView class
        # upload zip maybe?
        self.client.post(base_url + 'upload/zip', {'Media type': '*/*', 'Content': 'en-x-demo2_ulb_mrk.zip'})
        self.response = self.client.post(base_url + 'get_source', {'language': 'en-x-demo', 'version': 'ESV', 'book': 'en'},
                                         format='json')
        r = str(self.response)
        # just checking for existence of .tr file extension
        self.assertIn(r, '.tr')
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

        result = str(self.response.data)
        print result

        # double check tr_path variable
        #self.assertTrue(os.path.exists(tr_path))
        self.take_object.delete()
        self.language_object.delete()
        self.book_object.delete()
        self.user_object.delete()
        self.comment_object.delete()

    def test_that_source_audio_in_tR_file_is_in_MP3_format(self):
        """Verify that source audio in tR file contains files with MP3 file ext. only"""
        self.book_object.save()
        self.user_object.save()
        self.comment_object.save()
        self.language_object.save()
        self.take_object.save()
        self.response = self.client.post(base_url + 'get_source/', {'language': 'en-x-demo', 'version': 'ESV', 'book': 'en'},
                                         format='json')

        result = str(self.response.data)
        print result

        ##fix directory location possibly if previous test doesn't work either
        if any(File.endswith(".mp3") for File in os.listdir(tr_path)):
            i = 1
        else:
            i = 0

        #self.assertTrue(i == 1)
        # assert that media/tmp file_path_mp3 contains mp3 files
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