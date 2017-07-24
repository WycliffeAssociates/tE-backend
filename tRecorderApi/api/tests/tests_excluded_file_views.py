from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Language, Book, User, Comment, Take, Chunk, Project, Chapter
import os
from sys import platform

base_url = 'http://127.0.0.1:8000/api/'
view_set_url = 'http://127.0.0.1:8000/api/exclude_files/'
my_file = 'en-x-demo2_ulb_b42_mrk_c06_v01-03_t11.wav'


class ExcludedFileViewTestCases(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.take_object = Take(location=my_file, is_publish = False, duration = 0, markers = True, rating = 2)
        self.language_object = Language(slug='en-x-demo', name='english')
        self.book_object = Book(name='english', booknum=5, slug = 'slug')
        self.user_object = User(name='testy', agreed=True, picture='mypic.jpg')
        self.comment_object = Comment(location='/test-location/')
        self.chunk_object = Chunk(startv = 0, endv = 3)
        self.project_object = Project (is_source = False, is_publish = False, version = 'ulb', anthology = 'nt')
        self.chapter_object = Chapter(number = 1, checked_level = 1, is_publish = False)

    def test_post_method_for_excluded_file_view_set(self):
        """Unit Testing the method for handling POST requests to the API at the Excluded File View URL"""
        # populating our temporary database
        self.language_object.save()
        self.book_object.save()
        self.user_object.save()
        self.comment_object.save()
        self.take_object.save()
        response = self.client.post(view_set_url, {'location': my_file}, format='json')
        result = str(response.data)  # convert data returned from post request to string so we can checkthe data inside
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)  # testing that we get the correct status response from the API
        self.assertNotEqual(0, len(response.data))  # testing that we do not get an empty response from the api
        self.assertIn(my_file, result)  # test that data returned matches location of file
        # cleaning out our temporary database
        self.language_object.delete()
        self.book_object.delete()
        self.user_object.delete()
        self.comment_object.delete()
        self.take_object.delete()

    def integration_test_that_duplicate_wav_files_are_excluded_test(self):
        """Verify that hash function MD5 returns duplicate wav files"""
        # upload zip file that will be unzipped
        self.client.post(base_url + 'upload/zip', {'Media type': '*/*', 'Content': 'en-x-demo2_ulb_mrk.zip'}, format = 'zip')
        # post request to return list of wav files with same hash?
        self.response = self.client.post(base_url + 'exclude_files', {'version': 'ulb', 'location': my_file}, format='wav')
        # some duplicate file name(s) below with version ulb and the same location, depends on how response is returned
        self.assertIn('chapter.wav', self.response)

    def tearDown(self):
        if platform == "darwin":  # OSX
            os.system('rm -rf ' + 'media/export')  # cleaning out all files generated during tests
            os.system('mkdir ' + 'media/export')
        elif platform == "win32":  # Windows
            os.system('rmdir /s /q ' + 'media\export')  # cleaning out all files generated during tests
            os.system('mkdir ' + 'media\export')
