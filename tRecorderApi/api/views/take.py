from api.models import Take
from api.serializers import TakeSerializer
from rest_framework import viewsets


class TakeViewSet(viewsets.ModelViewSet):
    """This class handles the http GET, PUT, PATCH, POST and DELETE requests."""
    queryset = Take.objects.all()
    serializer_class = TakeSerializer

    def build_params_filter(self, query):
        pk = query.get("id", None)
        project_id = query.get("project_id", None)
        chapter_id = query.get("chapter_id", None)
        chunk_id = query.get("chunk_id", None)
        published = query.get("published", None)
        lang = query.get("lang", None)

        filter = {}
        if pk is not None:
            filter["id"] = pk
        if project_id is not None:
            filter["chunk__chapter__project"] = project_id
        if chapter_id is not None:
            filter["chunk__chapter"] = chapter_id
        if chunk_id is not None:
            filter["chunk"] = chunk_id
        if published is not None:
            filter['published'] = published.title()
        if lang is not None:
            filter['chunk__chapter__project__language__slug'] = lang
        return filter

    def get_queryset(self):
        queryset = Take.objects.all()
        if self.request.query_params:
            filter = self.build_params_filter(self.request.query_params)
            if filter:
                return queryset.filter(**filter)
            return None
        return queryset
