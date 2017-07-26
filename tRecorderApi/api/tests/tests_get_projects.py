from django.test import TestCase
from api.models import Take, Language, Book, User, Comment, Chunk, Project, Chapter
from rest_framework.test import APIClient
from rest_framework import status
import os
from sys import platform

view_url = 'http://127.0.0.1:8000/api/get_project_takes/'
base_url = 'http://127.0.0.1:8000/api/'
my_file = 'media/dump'

class GetProjectsTestCases(TestCase):

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
        self.project_takes_data = {"language": "en-x-demo2", "version": "ulb", "book": "mrk", "chapter": 1}

    def test_that_we_can_get_projects(self):
        """Testing that submitting a POST request through key search returns a JSON object"""
        # saving objects in temporary database so they can be read by the API
        self.language_object.save()
        self.book_object.save()
        self.project_object.save()
        self.chapter_object.save()
        self.chunk_object.save()
        self.user_object.save()
        self.take_object.save()
        self.response = self.client.post(view_url, self.project_takes_data ,
                                    format='json')
        # telling the API that I want all takes that are saved on the specified location
        result = str(self.response.data)  # convert data returned from post request to string so we can checkthe data inside
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)  # verifying that that we succesfully post to the API
        self.assertIn("en-x-demo2",
                      result)  # test that the term we searched for is in the data returned from the post request

    def test_that_we_can_get_no_projects_from_api(self):
        """Testing that getting a project that does not exist from not enough parameters posted"""
        # saving objects in temporary database so they can be read by the API
        self.language_object.save()
        self.book_object.save()
        self.project_object.save()
        self.chapter_object.save()
        self.chunk_object.save()
        self.user_object.save()
        self.take_object.save()
        response = self.client.post(view_url, {'location': my_file},
                                    format='json')
        # getting 400 error not enough parameters returned
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # verifying that that we succesfully post to the API
        self.take_object.delete()
        self.user_object.delete()
        self.book_object.delete()


    def tearDown(self):
        if platform == "darwin":  # OSX
            os.system('rm -rf ' + my_file)  # cleaning out all files generated during tests
            os.system('mkdir ' + my_file)
        elif platform == "win32":  # Windows
            os.system('rmdir /s /q ' + 'media\dump')  # cleaning out all files generated during tests
            os.system('mkdir ' + 'media\dump')