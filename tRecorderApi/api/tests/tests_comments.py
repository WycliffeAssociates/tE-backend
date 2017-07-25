from django.test import TestCase
from api.models import Comment, Project, Take, User, Book, Language, Chunk, Chapter
from api.views import CommentViewSet
from rest_framework.test import APIClient
from rest_framework import status

base_url = 'http://127.0.0.1:8000/api/'
my_file = 'media/dump'


class IntegrationCommentTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.language_object = Language(slug='en-x-demo', name='english')
        self.book_object = Book(name='english', booknum=5, slug='slug')
        self.project_object = Project(version='ulb', mode='audio', anthology='nt', is_source=False)
        self.chapter_object = Chapter(number=1, checked_level=1, is_publish=False)
        self.chunk_object = Chunk(startv=0, endv=3)
        self.take_object = Take(location=my_file, is_publish=False, duration=0, markers=True, rating=2)
        self.user_object = User(name='testy', agreed=True, picture='mypic.jpg')
        self.comment_object = Comment(location='test-location',
                                      object_id=1, content_type_id=10)
        self.comment_data = {'object': self.take_object.id, 'type': 'take', 'user': self.user_object.id, 'comment': "3" }
        self.commentVS = CommentViewSet()

    def test_api_can_create_comment_object(self):
        """Test the API has comment creation capability:
        Sending JSON Comment Object To API and
        Expecting HTTP Success Message Returned"""
        self.language_object.save()
        self.book_object.save()
        self.project_object.save()
        self.chapter_object.save()
        self.chunk_object.save()
        self.take_object.save()
        self.user_object.save()
        #self.response = self.client.post(base_url + 'comments/', self.comment_data, format='json')  # send POST to API
        #self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_update_comment_object(self):
        """Test that the API can update a User object:
        Sending User Object To API and
        Expecting HTTP Success Message Returned"""
        self.comment_object.save()
        self.client.post(base_url + 'comments/1/', self.comment_data, format='json')  # send POST to API
        self.response = self.client.patch(base_url + 'comments/1/', {'content_type_id': 2}, format='json')
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.comment_object.delete()  # delete object from temporary database
        self.assertEqual(0, len(Comment.objects.filter(content_type_id=2)))

    def test_get_comment_request_returns_success(self):
        """Testing API can handle GET requests for Comment objects"""
        self.comment_object.save()
        response = self.client.get(base_url + 'comments/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.comment_object.delete()  # delete object from temporary database
        self.assertEqual(0, len(Comment.objects.filter(id=1)))  # check that object was deleted from temporary database

    def test_that_api_can_delete_comment_objects(self):
        """Testing that the API has Comment Object deletion functionality"""
        self.comment_object.save()
        response = self.client.delete(base_url + 'comments/1/')
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)  # after deleting an object, nothing should be returned, which is why we check against a 204 status code
        self.comment_object.delete()
