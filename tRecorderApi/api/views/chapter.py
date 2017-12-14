from api.models import Chapter
from rest_framework import viewsets
from api.serializers import ChapterSerializer

class ChapterViewSet(viewsets.ModelViewSet):
    """This class handles the http GET, PUT, PATCH, POST and DELETE requests."""
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

    def build_params_filter(self, query):
        pk = query.get("id", None)
        project_id = query.get("project_id", None)
        published = query.get("published", None)
        filter = {}
        if pk is not None:
            filter["id"] = pk
        if project_id is not None:
            filter["project"] = project_id
        if published is not None:
            filter["published"] = published=='true'
        return filter

    def get_queryset(self):
        queryset = Chapter.objects.all()
        pk = self.kwargs.get("pk", None)
        if pk is not None:
            print(pk)
            return Chapter.objects.filter(id=pk)
        else:
            filter = self.build_params_filter(self.request.query_params)
            return queryset.filter(**filter)
