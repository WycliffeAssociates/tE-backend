from api.models import Anthology
from rest_framework import viewsets
from api.serializers import AnthologySerializer

class AnthologyViewSet(viewsets.ModelViewSet):
    """This class handles the http GET, PUT, PATCH, POST and DELETE requests."""
    queryset = Anthology.objects.all()
    serializer_class = AnthologySerializer

    def build_params_filter(self, query):
        pk = query.get("id", None)
        slug = query.get("slug", None)
        filter = {}
        if pk is not None:
            filter["id"] = pk
        if slug is not None:
            filter["slug__iexact"] = slug
        return filter

    def get_queryset(self):
        queryset = Anthology.objects.all()
        pk = self.kwargs.get("pk", None)
        if pk is not None:
            print(pk)
            return Anthology.objects.filter(id=pk)
        else:
            filter = self.build_params_filter(self.request.query_params)
            return queryset.filter(**filter)
