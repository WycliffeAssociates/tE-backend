from django.test import TestCase
from api.models import Take, Language, Book, User, Comment, Chunk, Project, Chapter
from rest_framework.test import APIClient
from rest_framework import status

view_url = 'http://127.0.0.1:8000/api/get_chapters/'
my_file = 'en-x-demo2_ulb_b42_mrk_c06_v01-03_t11.wav'


class ProjectChapterInfoViewTestCases(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.language_object = Language(slug='en-x-demo', name='english')
        self.book_object = Book(name='english', booknum=5, slug='slug')
        self.project_object = Project(version='ulb', mode='audio', anthology='nt', is_source=False)
        self.chapter_object = Chapter(number=1, checked_level=1, is_publish=False)
        self.chunk_object = Chunk(startv=0, endv=3)
        self.take_object = Take(location=my_file, is_publish=False, duration=0, markers=True, rating=2)
        self.user_object = User(name='testy', agreed=True, picture='mypic.jpg')
        self.comment_object = Comment(location='/test-location/', content_type_id=1, object_id=1)


    def test_post_request_for_project_chapter_info_view(self):
        """Testing POST request where we include metadata from a take to search for all chapters and get the data for those chapters back"""
        self.language_object.save()
        self.book_object.save()
        self.user_object.save()
        self.take_object.save()
        response = self.client.post(view_url, {'language': 'en-x-demo', 'version': 'ESV', 'book': 'en'}, format='json')
        result = str(response.data)  # converting response data to string so we can view what's in the data
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)  # checking that we get the correct response back from api
        self.assertNotEqual(0, len(response.data))  # checking that the response contains data
        self.assertIn("'chapter': 5",
                      result)  # test that the term we searched for is in the data returned from the post request
        self.take_object.delete()
        self.user_object.delete()
        self.book_object.delete()
