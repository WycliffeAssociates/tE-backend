from api.models import Project
from rest_framework import viewsets
from api.serializers import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    """This class handles the http GET, PUT, PATCH, POST and DELETE requests."""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def build_params_filter(self, query):
        pk = query.get("id", None)
        published = query.get("published", None)
        lang = query.get("lang", None)
        version = query.get("version", None)
        book = query.get("book", None)
        mode = query.get("mode", None)
        anth = query.get("anth", None)
        filter = {}
        if pk is not None:
            filter["id"] = pk
        if published is not None:
            filter["published"] = published.title()
        if lang is not None:
            filter["language__slug__iexact"] = lang
        if version is not None:
            filter["version__slug__iexact"] = version
        if book is not None:
            filter["book__slug__iexact"] = book
        if mode is not None:
            filter["mode__slug__iexact"] = mode
        if anth is not None:
            filter["anthology_slug_iexact"] = anth
        return filter

    def get_queryset(self):
        queryset = Project.objects.all()
        if self.request.query_params:
            filter = self.build_params_filter(self.request.query_params)
            if filter:
                return queryset.filter(**filter)
            return None
        return queryset
