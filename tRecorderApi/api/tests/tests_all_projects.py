from django.test import TestCase
from api.models import Take, Language, Book, User, Comment, Chunk, Chapter, Project
from rest_framework.test import APIClient
from rest_framework import status

view_url = 'http://127.0.0.1:8000/api/all_projects/'


class AllProjectViewTestCases(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.take_object = Take(location = 'my_file', is_publish = False, duration = 0, markers = True, rating = 2)
        self.language_object = Language(slug='en-x-demo', name='english')
        self.book_object = Book(name='english', booknum=5, slug = 'slug')
        self.user_object = User(name='testy', agreed=True, picture='mypic.jpg', id=1)
        self.comment_object = Comment(location='/test-location/', content_type_id = 1, object_id = 1)
        self.chunk_object = Chunk(startv = 0, endv = 3)
        self.project_object = Project (is_source = False, is_publish = False, version = 'ulb', anthology = 'nt')
        self.chapter_object = Chapter(number = 1, checked_level = 1, is_publish = False)

    def test_post_request_for_all_projects_view(self):
        """Testing that sending a POST request to the All Project View returns a list of projects"""
        self.language_object.save()
        self.book_object.save()
        self.user_object.save()
        self.take_object.save()
        response = self.client.post(view_url, {'language': 'en-x-demo', 'version': 'ESV', 'book': 'en'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(0, len(response.data))  # checking that the response contains data
        self.take_object.delete()
        self.user_object.delete()
        self.book_object.delete()
