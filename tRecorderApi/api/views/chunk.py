from api.models import Chunk
from rest_framework import viewsets
from api.serializers import ChunkSerializer

class ChunkViewSet(viewsets.ModelViewSet):
    """This class handles the http GET, PUT, PATCH, POST and DELETE requests."""
    queryset = Chunk.objects.all()
    serializer_class = ChunkSerializer

    def build_params_filter(self, query):
        pk = query.get("id", None)
        project_id = query.get("project_id", None)
        chapter_id = query.get("chapter_id", None)
        filter = {}
        if pk is not None:
            filter["id"] = pk
        if project_id is not None:
            filter["chapter__project"] = project_id
        if chapter_id is not None:
            filter["chapter"] = chapter_id
        return filter

    def get_queryset(self):
        queryset = Chunk.objects.all()
        pk = self.kwargs.get("pk", None)
        if pk is not None:
            print(pk)
            return Chunk.objects.filter(id=pk)
        else:
            filter = self.build_params_filter(self.request.query_params)
            return queryset.filter(**filter)
