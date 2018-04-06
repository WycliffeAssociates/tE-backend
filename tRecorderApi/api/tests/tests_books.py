from django.test import TestCase
from rest_framework.test import APIClient
from ..models import Book, Anthology
from ..serializers import BookSerializer


class IntegrationBookTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.anthology = Anthology.objects.create(
            slug='nt', name="new testament", id=1)
        self.anthology2 = Anthology.objects.create(
            slug='ot', name="old testament", id=2)
        self.book_1 = Book.objects.create(
            name='mark', number=5, slug='mrk', anthology=self.anthology)
        self.book_2 = Book.objects.create(
            name='john', number=1, slug='jhn', anthology=self.anthology)
        self.book_2 = Book.objects.create(
            name='genesis', number=1, slug='gem', anthology=self.anthology2)
        self.book_serializer = BookSerializer(instance=self.book_1)

    def test_get_book(self):
        """
            Verify that the BookSerializer class serializes an object of type
            'Book' into a JSON format containing the following assumed keys:
                1) id
                2) slug
                3) name
                4) book_num
            Input: data = serialized data of book object created in setup
            Expected: data will contain all of the keys listed above
        """
        data = self.book_serializer.data
        self.assertIn("id", data)
        self.assertIn("slug", data)
        self.assertIn("name", data)
        self.assertIn("number", data)

    # def test_get_book(self):
        # book_filter = Book.objects \
            # .filter(slug__iexact="mrk", anthology__slug__iexact="nt")
        # get_book = Book.get_books(book_filter)
        # for book in get_book:
            # self.assertIn("id", book)
            # self.assertIn("slug", book)
            # self.assertIn("name", book)
            # self.assertIn("book_num", book)
