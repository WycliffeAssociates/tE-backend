from django.test import TestCase
from api.models import Take, Chapter, Project, Chunk, Book, Language,User,Comment
from rest_framework.test import APIClient
from rest_framework import status

base_url = 'http://127.0.0.1:8000/api/'
my_file = 'media/dump'

class IntegrationTakeTestCases(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.language_object = Language(slug='en-x-demo', name='english')
        self.book_object = Book(name='genesis', booknum=5, slug='gen')
        self.project_object = Project(version='ulb', mode='chunk',
                                      anthology='nt', is_source=False, language=self.language_object,
                                      book=self.book_object)
        self.chapter_object = Chapter(number=1, checked_level=1, is_publish=False, project=self.project_object)
        self.chunk_object = Chunk(startv=0, endv=3, chapter=self.chapter_object)
        self.user_object = User(name='testy', agreed=True, picture='mypic.jpg')
        self.take_object = Take(location=my_file, is_publish=True,
                                duration=0, markers=True, rating=2, chunk=self.chunk_object, user=self.user_object)

    def test_api_can_create_take_object(self):
        """Test the API has take creation capability:
        Sending JSON Take Object To API and
        Expecting HTTP Success Message Returned"""
        self.language_object.save()
        self.book_object.save()
        self.project_object.save()
        self.chapter_object.save()
        self.chunk_object.save()
        self.user_object.save()
        #self.response = self.client.post(base_url + 'takes/', self.take_data, format='json')  # send POST to API
        #self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_update_take_object(self):
        """Test that the API can update a take object:
        Sending Take Object To API and
        Expecting HTTP Success Message Returned"""
        self.language_object.save()
        self.book_object.save()
        self.project_object.save()
        self.chapter_object.save()
        self.chunk_object.save()
        self.user_object.save()
        self.take_object.save()
        self.response = self.client.patch(base_url + 'takes/1/', {'rating': 1}, format='json')
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.take_object.delete()
        self.assertEqual(0, len(Take.objects.filter(duration=3)))

    def test_get_take_request_returns_success(self):
        """Testing API can handle GET requests for Take objects"""
        self.language_object.save()
        self.book_object.save()
        self.project_object.save()
        self.chapter_object.save()
        self.chunk_object.save()
        self.user_object.save()
        self.take_object.save()
        response = self.client.get(base_url + 'takes/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.take_object.delete()


    def test_that_api_can_delete_take_objects(self):
        """Testing that the API has Take Object deletion functionality"""
        self.language_object.save()
        self.book_object.save()
        self.project_object.save()
        self.chapter_object.save()
        self.chunk_object.save()
        self.user_object.save()
        self.take_object.save()
        self.response = self.client.delete(base_url + 'takes/1/')
        self.assertEqual(self.response.status_code,
                         status.HTTP_200_OK)   # check that take_object was deleted from temporary database
        self.assertEqual(0,
                         len(Take.objects.filter(id=1)))
        self.take_object.delete()
