from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from ...models import Language, Anthology, Book, Version, Mode, Project, Chapter, Chunk


class ChunkApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.lang = Language.objects.create(slug='en-x-demo', name='english')
        self.anthology = Anthology.objects.create(slug='ot', name="old testament")
        self.book = Book.objects.create(name='mark', number=5, slug='mrk', anthology=self.anthology)
        self.version = Version.objects.create(slug='ulb', name="Unlocked literal bible")
        self.mode = Mode.objects.create(slug="chk", name="chunk", unit=1)
        self.project = Project.objects.create(version=self.version, mode=self.mode,
                                              anthology=self.anthology, language=self.lang,
                                              book=self.book)

        self.chap = Chapter.objects.create(number=1, checked_level=1, published=False, project=self.project)
        self.chap2 = Chapter.objects.create(number=2, checked_level=2, published=False, project=self.project)

        self.chunk = Chunk.objects.create(startv=0, endv=3, chapter=self.chap)
        self.chunk2 = Chunk.objects.create(startv=0, endv=3, chapter=self.chap2)

    def test_number_of_items_are_equal(self):
        chapter_num = Chunk.objects.count()
        response = self.client.get('/api/chunks/')
        self.assertEqual(len(response.data), chapter_num)

    def test_get_request_has_200_status_code(self):
        response = self.client.get('/api/chunks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_request_with_id_has_200_status_code(self):
        response = self.client.get('/api/chunks/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_request_with_id_has_200_status_code(self):
        response = self.client.get('/api/chunks/?id=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_request_with_non_existent_id_has_404_status_code(self):
        response = self.client.get('/api/chunks/4/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_random_text_as_parameter_gives_400_status_code(self):
        response = self.client.get('/api/chunks/?randomeparameter/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_response_contains_project(self):
        response = self.client.get('/api/chunks/')
        self.assertContains(response.data, self.project)
