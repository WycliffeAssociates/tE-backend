from django.test import TestCase
from api.models import Take, Language, Book, User, Comment, Chunk, Project, Chapter
from rest_framework.test import APIClient
from rest_framework import status
import os
from sys import platform

view_url = 'http://127.0.0.1:8000/api/get_project_takes/'
my_file = 'media/dump'

class GetProjectsTestCases(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.take_object = Take(location=my_file, is_publish = False, duration = 0, markers = True, rating = 2)
        self.language_object = Language(slug='en-x-demo', name='english')
        self.book_object = Book(name='english', booknum=5, slug = 'slug')
        self.user_object = User(name='testy', agreed=True, picture='mypic.jpg')
        self.comment_object = Comment(location='/test-location/', content_type_id = 1, object_id = 1)
        self.chunk_object = Chunk(startv = 0, endv = 3)
        self.project_object = Project (is_source = False, is_publish = False, version = 'ulb', anthology = 'nt')
        self.chapter_object = Chapter(number = 1, checked_level = 1, is_publish = False)

    def test_that_we_can_get_projects(self):
        """Testing that submitting a POST request through key search returns a JSON object"""
        # saving objects in temporary database so they can be read by the API
        self.language_object.save()
        self.book_object.save()
        self.user_object.save()
        self.take_object.save()
        response = self.client.post(view_url, {'location': my_file},
                                    format='json')
        # telling the API that I want all takes that are saved on the specified location
        result = str(response.data)  # convert data returned from post request to string so we can checkthe data inside
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # verifying that that we succesfully post to the API
        self.assertIn("'is_source': False",
                      result)  # test that the term we searched for is in the data returned from the post request
        # freeing up the temporary database
        self.take_object.delete()
        self.user_object.delete()
        self.book_object.delete()

    def test_that_we_can_get_no_projects_from_api(self):
        """Testing that getting a project that does not exist from key value returns no object"""
        # saving objects in temporary database so they can be read by the API
        self.language_object.save()
        self.book_object.save()
        self.user_object.save()
        self.take_object.save()
        response = self.client.post(view_url, {'location': my_file},
                                    format='json')
        # telling the API that I want all takes that has my_file as a location, which there should be none of
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # verifying that that we succesfully post to the API
        self.assertEqual(0, len(response.data))
        self.assertEqual(response.data, [])
        # freeing up the temporary database
        self.take_object.delete()
        self.user_object.delete()
        self.book_object.delete()
        
    def test_that_we_can_get_a_project_from_language_key(self):
        """Testing that submitting a POST request through language key search returns on object"""
        # saving objects in temporary database so they can be read by the API
        self.language_object.save()
        self.book_object.save()
        self.user_object.save()
        self.take_object.save()
        response = self.client.post(view_url, {'language': 'english'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # verifying that that we succesfully post to the API
        self.assertEqual(0, len(response.data))
        # freeing up the temporary database
        self.take_object.delete()
        self.user_object.delete()
        self.book_object.delete()

    def test_that_we_can_get_correct_project_from_book_key(self):
        """Testing that submitting a POST request through book key search returns an object"""
        # saving objects in temporary database so they can be read by the API
        self.language_object.save()
        self.book_object.save()
        response = self.client.post(view_url, {'book': 'english'},
                                    format='json')  # telling the API that I want all takes that are in book English
        self.assertEqual(0, len(response.data))
        # freeing up the temporary database
        self.language_object.delete()
        self.book_object.delete()

    def test_that_we_can_get_no_projects_from_api(self):
         """Testing that submitting a POST request to get projects JSON data that can be parsed into takes"""
         #saving objects in temporary database so they can be read by the API
         self.language_object.save()
         self.book_object.save()
         self.user_object.save()
         self.take_object.save()
         response = self.client.post(view_url, {'location' : "/bad_location"}, format='json') #telling the API that I want all takes that have chapter 6 of a book recorded, which there shoul be none of
         self.assertEqual(response.status_code, status.HTTP_200_OK) #verifying that that we succesfully post to the API
         self.assertEqual(0, len(response.data))
         self.assertEqual(response.data, [])
         #freeing up the temporary database
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