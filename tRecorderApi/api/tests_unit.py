from django.test import TestCase
from models import Take, Language, Book, User, Comment
from rest_framework.test import APIClient
from rest_framework import status
import os
from sys import platform
import json
import hashlib
import os.path
from views_sets import md5Hash
import glob


base_url = 'http://127.0.0.1:8000/api/'
my_file = 'media/dump'
export_path = '/Users/nicholasdipinto1/Desktop/translationDB/8woc2017backend/tRecorderApi/en-x-demo2_ulb_mrk.zip'
tr_path = 'media/tmp/english_ulb.tr'
#import views_sets and test methods associated with views_sets


class ViewTestCases(TestCase):
    def setUp(self):
        """Set up environment for api view test suite"""
        self.client = APIClient()
        self.take_data = {'location' : 'my_file', 'chapter' : 5, 'is_export' : True, 'is_source' : False}
        self.lang_data = {'lang' : 'english', 'code' : 'abc'}
        self.user_data = {'name' : 'tester', 'agreed' : True, 'picture' : 'test.pic'}
        self.comment = {'location':'my_file'}
        self.book_data = {'code':'ex', 'name' : 'english', 'booknum' : 5}
        self.take_object = Take(location= 'my_file', chapter=5, is_export=True, is_source=False, id=1, language_id=1, book_id=1, user_id=1)
        self.language_object = Language(slug='en-x-demo', name='english', id=1)
        self.book_object = Book(name='english', booknum=5, id=1)
        self.user_object = User(name='testy', agreed=True, picture='mypic.jpg', id=1)
        self.comment_object = Comment(location='/test-location/', id=1)

    ################################# Hash check in helpers.py ##########################

    def unit_testing_md5Hash_method_for_equality_with_duplicate_wav_files(self):
        # create object later when this is added to views_sets.py
        # helpers.md5Hash('chapter.wav')
        # helpers.md5Hash('chapter.wav')
        self.assertEqual(md5Hash('chapter.wav'), md5Hash('chapter.wav'))

    def unit_testing_md5Hash_method_for_inequality_with_different_wav_files(
            self):  # create object later when this is in views_sets.py
        hash1 = md5Hash('language.json')
        hash2 = md5Hash('en-x-demo2_ulb_b42_mrk_c07_v33-35_t04.wav')
        self.assertEqual(hash1, hash2)
        # helpers.md5Hash('language.json')

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
        self.client.post(base_url + 'get_source', {'language': 'chinese', 'version': 'ulb'},
                         format='json')
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
        if any(File.endswith(".mp3") for File in os.listdir(tr_path)):
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
        self.client.post(base_url + 'upload/zip', {'Media type': '*/*', 'Content': 'en-x-demo2_ulb_mrk.zip'}, format = 'zip')
        # post request to return list of wav files with same hash?
        self.response = self.client.post(base_url + 'exclude_files', {'version': 'ulb', 'chapter': '7'}, format='wav')
        # some duplicate file name(s) below with version ulb and chapter 7, depends on how response is returned
        self.assertIn('chapter.wav', self.response)

 ############################### source file upload error check ########################

    def test_that_we_get_403_error_when_not_enough_parameters_are_uploaded_in_SourceFile(self):
        """Testing that submitting a POST request through book key search returns an object"""
        # saving objects in temporary database so they can be read by the API
        self.response = self.client.post(base_url + 'get_source/', {'book': 'book', 'book': 'book'},
                                    format='json')  # telling the API that I want all takes that are in book English
        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)
        # freeing up the temporary database

    def test_that_we_get_403_error_when_no_source_is_uploaded_in_SourceFile(self):
        """Testing that submitting a POST request through book key search returns an object"""
        # saving objects in temporary database so they can be read by the API
        self.response = self.client.post(base_url + 'get_source/', {'language': 'eng', 'version': 'ulb'},
                                    format='json')  # telling the API that I want all takes that are in book English
        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)

####################### Project zip File error check ##################

    def test_that_we_get_403_error_when_not_enough_parameters_in_ProjectZipFile(self):
        """Testing that submitting a POST request through book key search returns an object"""
        # saving objects in temporary database so they can be read by the API
        self.response = self.client.post(base_url + 'zipFiles/', {'language': 'eng', 'version': 'ulb'},
                                    format='json')  # telling the API that I want all takes that are in book English
        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)

    def test_that_we_get_202_when_enough_parameters_in_ProjectZipFile(self):
        """Testing that submitting a POST request through book key search returns an object"""
        # saving objects in temporary database so they can be read by the API
        self.response = self.client.post(base_url + 'zipFiles/', {'language': 'eng', 'version': 'ulb', 'book':'gen'},
                                    format='json')  # telling the API that I want all takes that are in book English
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def tearDown(self):
        if platform == "darwin": #OSX
            os.system('rm -rf ' + my_file)  # cleaning out all files generated during tests
            os.system('mkdir ' + my_file)
        elif platform == "win32": #Windows
            os.system('rmdir /s /q ' + 'media\dump')  # cleaning out all files generated during tests
            os.system('mkdir ' + 'media\dump')
