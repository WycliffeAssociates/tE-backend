from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Language, Book, User, Comment, Take, Chunk, Project, Chapter
import os
from sys import platform
from django.conf import settings

base_url = 'http://127.0.0.1:8000/api/'
view_set_url = 'http://127.0.0.1:8000/api/exclude_files/'
my_file = settings.BASE_DIR + "/en-x-demo2_ulb_b42_mrk_c06_v01-03_t11.wav"


class ExcludedFileViewTestCases(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.language_object = Language(slug='en-x-demo2', name='english')
        self.book_object = Book(name='mark', booknum=5, slug='mrk')
        self.project_object = Project(version='ulb', mode='chunk',
                                      anthology='nt', is_source=False, language=self.language_object,
                                      book=self.book_object)
        self.chapter_object = Chapter(number=1, checked_level=1, is_publish=False, project=self.project_object)
        self.chunk_object = Chunk(startv=1, endv=3, chapter=self.chapter_object)
        self.user_object = User(name='testy', agreed=True, picture='mypic.jpg')
        self.take_object = Take(location=my_file, is_publish=True,
                                duration=0, markers=True, rating=2, chunk=self.chunk_object, user=self.user_object)

    def test_post_method_for_excluded_file_view_set(self):
        """Unit Testing the method for handling POST requests to the API at the Excluded File View URL"""
        # populating our temporary database
        self.language_object.save()
        self.book_object.save()
        self.project_object.save()
        response = self.client.post(view_set_url, {"version":"ulb"}, format='json')
        result = str(response.data)  # convert data returned from post request to string so we can check the data inside
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)  # testing that we get the correct status response from the API
        self.language_object.delete()
        self.book_object.delete()
        self.project_object.delete()

    #doesn't run yet
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
            os.system('rm -rf ' + settings.BASE_DIR + '/media/export')  # cleaning out all files generated during tests
            os.system('mkdir ' + settings.BASE_DIR + '/media/export')
        elif platform == "win32":  # Windows
            os.system('rmdir /s /q ' + settings.BASE_DIR + '\media\export')  # cleaning out all files generated during tests
            os.system('mkdir ' + settings.BASE_DIR + '\media\export')
