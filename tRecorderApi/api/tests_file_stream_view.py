from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from models import Take, Language, Book, User, Comment

view_set_url = 'http://127.0.0.1:8000/api/exclude_files/'
my_file = 'en-x-demo2_ulb_b42_mrk_c06_v01-03_t11.wav'

class FileStreamViewTestCases(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.take_object = Take(location= my_file, chapter=5, is_export=True, is_source=False, id=1, language_id=1, book_id=1, user_id=1)
        self.language_object = Language(slug='en-x-demo', name='english', id=1)
        self.book_object = Book(name='english', booknum=5, id=1)
        self.user_object = User(name='testy', agreed=True, picture='mypic.jpg', id=1)
        self.comment_object = Comment(location='/test-location/', id=1)