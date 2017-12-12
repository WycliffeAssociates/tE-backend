from api.models import Book
from api.serializers import BookSerializer
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import views, status


class BookViewSet(viewsets.ModelViewSet):
    """This class handles the http GET, PUT, PATCH, POST and DELETE requests."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer


