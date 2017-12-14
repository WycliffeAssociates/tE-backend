from api.models import Comment
from rest_framework import viewsets, status
from rest_framework.response import Response
from api.serializers import CommentSerializer
import os, re, base64

class CommentViewSet(viewsets.ModelViewSet):
    """This class handles the http GET, PUT, PATCH, POST and DELETE requests."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.all()
        pk = self.kwargs.get("pk", None)
        if pk is not None:
            print(pk)
            return Comment.objects.filter(id=pk)
        else:
            query = self.request.query_params
            pk = query.get("id", None)
            chapter_id = query.get("chapter_id", None)
            chunk_id = query.get("chunk_id", None)
            take_id = query.get("take_id", None)
            filter = {}
            if pk is not None:
                filter["id"] = pk
            if chapter_id is not None:
                queryset = Comment.get_comments(chapter_id=chapter_id)
            if chunk_id is not None:
                queryset = Comment.get_comments(chunk_id=chunk_id)
            if take_id is not None:
                queryset = Comment.get_comments(take_id=take_id)


    def destroy(self, request, pk=None):
        instance = self.get_object()
        try:
            os.remove(instance.location)
        except OSError:
            pass
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)

    def blob2base64Decode(self, str):
        return base64.decodestring(re.sub(r'^(.*base64,)', '', str))
