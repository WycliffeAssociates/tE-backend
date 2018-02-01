from api.models import Book
from api.serializers import BookSerializer
from rest_framework import viewsets


class BookViewSet(viewsets.ModelViewSet):

    """This class handles the http GET, PUT, PATCH, POST and DELETE requests."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def build_params_filter(self, query):
        pk = query.get("id", None)
        slug = query.get("slug", None)
        anth = query.get("anth", None)
        num = query.get("num", None)
        filter = {}
        if pk is not None:
            filter["id"] = pk
        if slug is not None:
            filter["slug__iexact"] = slug
        if anth is not None:
            filter["anthology__slug__iexact"] = anth
        if num is not None:
            filter["number"] = num
        return filter

    def get_queryset(self):
        queryset = Book.objects.all()
        if self.request.query_params:
            filter = self.build_params_filter(self.request.query_params)
            if filter:
                return queryset.filter(**filter)
            return None
        return queryset
