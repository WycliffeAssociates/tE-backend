from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
import random
import string

from ..models import Language, Anthology, Book, Version, Mode, Project, Chapter, Chunk, Take


class TakesApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.lang = Language.objects.create(slug='yo', name='yolo')
        self.anthology = Anthology.objects.create(slug='ot', name="old testament")
        self.book = Book.objects.create(name='mark', number=5, slug='mrk', anthology=self.anthology)
        self.version = Version.objects.create(slug='ulb', name="Unlocked literal bible")
        self.mode = Mode.objects.create(slug="chk", name="chunk", unit=1)
        self.proj = Project.objects.create(version=self.version, mode=self.mode,
                                           anthology=self.anthology, language=self.lang,
                                           book=self.book)
        self.chap = Chapter.objects.create(number=1, checked_level=1, published=False, project=self.proj)
        self.chunk = Chunk.objects.create(startv=0, endv=3, chapter=self.chap)
        self.take = Take.objects.create(location="take1.mp3", published=True,
                                        duration=0, markers="{\"test\" : \"true\"}", rating=2, chunk=self.chunk
                                        )
        self.random_url = ''.join(random.choices(string.ascii_uppercase +
                                                 string.digits,
                                                 k=random.randint(1,15)))

    def test_number_of_items_are_equal(self):
        language_num = Take.objects.count()
        response = self.client.get('/api/takes/')
        self.assertEqual(len(response.data), language_num)

    def test_get_request_has_200_status_code(self):
        response = self.client.get('/api/takes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_request_with_id_has_200_status_code(self):
        response = self.client.get('/api/takes/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_request_with_id_has_200_status_code(self):
        response = self.client.get('/api/takes/?id=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_request_with_non_existent_id_has_404_status_code(self):
        response = self.client.get('/api/takes/4/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_random_text_as_parameter_gives_400_status_code(self):
        response = self.client.get('/api/takes/?'+self.random_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rating_is_updated(self):
        self.client.patch('/api/takes/1/', {"rating": 1})
        take = Take.objects.get(id=1)
        self.assertEqual(take.rating, 1)

    def test_published_is_updated(self):
        self.client.patch('/api/takes/1/', {"published": False})
        take = Take.objects.get(id=1)
        self.assertFalse(take.published)
