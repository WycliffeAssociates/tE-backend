from django.test import TestCase
from api.models import Take, Language, Book, User, Comment, Chunk, Chapter, Project
from rest_framework.test import APIClient
from rest_framework import status

view_url = 'http://127.0.0.1:8000/api/all_projects/'

class AllProjectViewTestCases(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.language_object = Language(slug='en-x-demo2', name='english')
        self.book_object = Book(name='mark', booknum=5, slug='mrk')
        self.project_object = Project(version='ulb', mode='chunk',
                                      anthology='nt', is_source=False, language=self.language_object,
                                      book=self.book_object)
        self.chapter_object = Chapter(number=1, checked_level=1, is_publish=False, project=self.project_object)
        self.chunk_object = Chunk(startv=0, endv=3, chapter=self.chapter_object)
        self.user_object = User(name='testy', agreed=True, picture='mypic.jpg')
        self.take_object = Take(location='my_file', is_publish=True, date_modified = "2017-07-25T15:20:50.169000Z",
                                duration=0, markers=True, rating=2, chunk=self.chunk_object, user=self.user_object)
        self.project_data = {"version": "ulb", "mode": "chunk", "anthology": "nt"}


    def test_post_request_for_all_projects_view(self):
        """Testing that sending a POST request to the All Project View returns a list of projects"""
        self.language_object.save()
        self.book_object.save()
        self.project_object.save()
        self.chapter_object.save()
        self.chunk_object.save()
        self.user_object.save()
        self.take_object.save()
        self.response = self.client.post(view_url,{"language":"en-x-demo2"}, format='json')
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        #check that response contains data
        self.assertNotEqual(0,len(str(self.response)))
        self.book_object.delete()
        self.language_object.delete()
        self.project_object.delete()
        self.chapter_object.delete()
        self.chunk_object.delete()
        self.user_object.delete()
        self.take_object.delete()
