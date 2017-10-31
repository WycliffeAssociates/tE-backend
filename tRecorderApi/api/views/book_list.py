from rest_framework import views, status
from rest_framework.parsers import JSONParser
import json
from api.models import Take, Language, Book
from rest_framework.response import Response
from operator import itemgetter
from ..models import Book


class getBooksView(views.APIView):
    parser_classes = (JSONParser,)

    def post(self, request):
        data = request.data
        if "slug" in data:
            book_filter = Book.objects.filter(slug__iexact=data["slug"])
        if "anthology" in data:
            book_filter = Book.objects.filter(anthology__slug__iexact=data["anthology"]["slug"])
        book = Book.get_books(book_filter)
        return Response(book, status=200)
