from api.models import Language
from rest_framework import viewsets
from api.serializers import LanguageSerializer


class LanguageViewSet(viewsets.ModelViewSet):
    """This class handles the http GET, PUT, PATCH, POST and DELETE requests."""
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

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
        queryset = Language.objects.all()
        if self.request.query_params:
            filter = self.build_params_filter(self.request.query_params)
            if filter:
                return queryset.filter(**filter)
            return None
        return queryset
