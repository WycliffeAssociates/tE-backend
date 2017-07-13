from django.test import TestCase
from datetime import datetime
from models import Take, Language, Book, User, Comment
from views_sets import SourceFileView, FileUploadView, FileStreamView
from rest_framework.test import APIClient
from rest_framework import status
import os
from sys import platform
import hashlib


base_url = 'http://127.0.0.1:8000/api/'
my_file = 'media/dump'
tr_path = 'media/tmp/english_ulb.tr'


class FileServerTests(TestCase):
    def SetUp(self):
        """Set up environment for fileServer test suite"""
        self.client = APIClient()
        self.take_object = Take(location='my_file', chapter=5, is_export=True, is_source=False, id=1, language_id=1,
                                book_id=1, user_id=1)
        self.language_object = Language(slug='en-x-demo', name='english', id=1)
        self.book_object = Book(name='english', booknum=5, id=1)
        self.user_object = User(name='testy', agreed=True, picture='mypic.jpg', id=1)
        self.comment_object = Comment.objects.create(location='/test-location/', id=1)

    def test_that_uploading_non_zip_file_returns_403_error(self):
        """Verify that uploading a non zip file will return a 403 FORBIDDEN code"""
        with open('Sample.docx', 'rb') as test_nonzip:
            self.response = self.client.post(base_url + 'upload/zip', {'Media type': '*/*', 'Content': test_nonzip},
                                             format='multipart')
            self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)

    def test_that_uploading_non_wav_file_returns_403_error(self):
        """Verify that uploading a zip file containing non .wav files returns 403 FORBIDDEN code"""
        with open('no_wav_files.zip', 'rb') as test_zip_nowav:
            self.response = self.client.post(base_url + 'upload/zip', {'Media type': '*/*', 'Content': test_zip_nowav},
                                             format='multipart')
            self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)

    ############################ Testing tr TDD ####################################

    def test_that_tR_file_was_returned_in_response_from_wav_files(self):
        """Verify that files are ready for exporting in a folder with file extension tR only"""
        self.take_object.save()
        self.language_object.save()
        # from SourceFileView class
        # upload zip maybe?
        self.client.post(base_url + 'upload/zip', {'Media type': '*/*', 'Content': 'en-x-demo2_ulb_mrk.zip'})
        self.response = self.client.post(base_url + 'get_source', {'language': 'english', 'version': 'ulb'},
                                         format='json')
        r = str(self.response)
        # just checking for existence of .tr file extension
        self.assertIn(r, '.tr')
        self.take_object.delete()
        self.language_object.save()

    def test_that_tR_is_in_correct_directory(self):
        """Verify that tR was created in correct directory"""
        self.take_object.save()
        self.language_object.save()
        self.response = self.client.post(base_url + 'get_source', {'language': 'english', 'version': 'ulb'},
                                         format='json')
        # double check tr_path variable
        self.assertTrue(os.path.exists(tr_path))
        self.take_object.delete()
        self.language_object.save()

    def test_that_source_audio_in_tR_file_is_in_MP3_format(self):
        """Verify that source audio in tR file contains files with MP3 file ext. only"""
        self.take_object.save()
        self.language_object.save()
        self.response = self.client.post(base_url + 'get_source', {'language': 'english', 'version': 'ulb'},
                                         format='json')
        ##fix directory location possibly if previous test doesn't work either
        if any(File.endswith(".mp3") and not any(File.endswith(".wav")) for File in os.listdir('tr_path')):
            i = 1
        else:
            i = 0
        self.assertTrue(i == 1)
        # assert that media/tmp file_path_mp3 contains mp3 files
        self.take_object.delete()
        self.language_object.save()

    ##################### duplicate wav file checking #################################

    def integration_test_that_duplicate_wav_files_are_excluded_test(self):  ####go back, TDD####
        """Verify that hash function MD5 returns duplicate wav files"""
        # upload zip file that will be unzipped
        self.client.post(base_url + 'upload/zip', {'Media type': '*/*', 'Content': 'en-x-demo2_ulb_mrk.zip'})
        # post request to return list of wav files with same hash?
        self.response = self.client.post(base_url + 'exclude_files', {'version': 'ulb', 'chapter': '7'}, format='wav')
        # some duplicate file name(s) below with version ulb and chapter 7, depends on how response is returned
        self.assertIn('chapter.wav', self.response)

    def unit_testing_md5Hash_method_for_equality_with_duplicate_wav_files(
            self):  # create object later when this is added to views_sets.py
        hash_md5a = hashlib.md5()
        with open('chapter.wav', "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5a.update(chunk)
        hash1 = hash_md5a.hexdigest()

        hash_md5b = hashlib.md5()
        with open('chapter.wav', "rb") as g:
            for chunk in iter(lambda: g.read(4096), b""):
                hash_md5b.update(chunk)
        hash2 = hash_md5b.hexdigest()

        self.assertEqual(hash1, hash2)

    def unit_testing_md5Hash_method_for_inequality_with_different_wav_files(
            self):  # create object later when this is in views_sets.py
        hash_md5a = hashlib.md5()
        with open('chapter.wav', "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5a.update(chunk)
        hash1 = hash_md5a.hexdigest()

        hash_md5b = hashlib.md5()
        with open('en-x-demo2_ulb_b42_mrk_c07_v33-35_t04.wav', "rb") as g:
            for chunk in iter(lambda: g.read(4096), b""):
                hash_md5b.update(chunk)
        hash2 = hash_md5b.hexdigest()

        self.assertNotEqual(hash1, hash2)

    def tearDown(self):
        if platform == "darwin":  # OSX
            os.system('rm -rf ' + my_file)  # cleaning out all files generated during tests
            os.system('mkdir ' + my_file)
        elif platform == "win32":  # Windows
            os.system('rmdir /s /q ' + 'media\dump')  # cleaning out all files generated during tests
            os.system('mkdir ' + 'media\dump')
