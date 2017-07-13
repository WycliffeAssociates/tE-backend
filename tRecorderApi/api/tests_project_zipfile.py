from django.test import TestCase
from models import Take, Language, Book, User, Comment
from rest_framework.test import APIClient
from rest_framework import status
import os
from sys import platform
import os.path

view_url = 'http://127.0.0.1:8000/api/zipFiles/'
my_file = 'en-x-demo2_ulb_b42_mrk_c06_v01-03_t11.wav'


class ProjectZipFileViewTestCases(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.take_object = Take(location=my_file, chapter=5, version='ESV', is_export=True, is_source=False, id=1,
                                language_id=1, book_id=1, user_id=1)
        self.language_object = Language(slug='en-x-demo', name='english', id=1)
        self.book_object = Book(name='Mark', slug='en', booknum=5, id=1)
        self.user_object = User(name='testy', agreed=True, picture='mypic.jpg', id=1)
        self.comment_object = Comment(location='/test-location/', id=1)

    def test_post_request_for_project_zip_file_view(self):
        """POST request for Project Zip File view expects a wav file as input, and will return a zip file"""
        self.language_object.save()
        self.book_object.save()
        self.user_object.save()
        self.take_object.save()
        old_folder_size = len(os.listdir('media/export'))  # find the total number of files in the media/export folder
        response = self.client.post(view_url, {'language': 'en-x-demo', 'version': 'ESV', 'book': 'en'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # making sure that we return the correct status code
        new_folder_size = len(os.listdir('media/export'))  # new zip file should have been added to media/export folder
        self.assertNotEqual(old_folder_size, new_folder_size)  # check that a new file exists in media/export
        self.take_object.delete()
        self.user_object.delete()
        self.book_object.delete()

    def tearDown(self):
        if platform == "darwin":  # OSX
            os.system('rm -rf ' + 'media/export')  # cleaning out all files generated during tests
            os.system('mkdir ' + 'media/export')
        elif platform == "win32":  # Windows
            os.system('rmdir /s /q ' + 'media\export')  # cleaning out all files generated during tests
            os.system('mkdir ' + 'media\export')
