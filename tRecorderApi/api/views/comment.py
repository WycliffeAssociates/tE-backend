from api.models import Comment
from rest_framework import viewsets, status
from api.serializers import CommentSerializer
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from helpers import getFilePath
from django.forms.models import model_to_dict
from api.models import Take, User
import os
import re

class CommentViewSet(viewsets.ModelViewSet):
    """This class handles the http GET, PUT, PATCH, POST and DELETE requests."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    parser_classes = (JSONParser, MultiPartParser)

    def create(self, request):
        
        comment = request.data["comment"]
        file = request.data["file"]
        user = request.data["user"]

        comment_ext = find_file_extension(comment.name)

        q_take = Take.objects.get(pk=file)
        q_user = User.objects.get(pk=user)
        q_last_comment = Comment.objects.filter(file=file) \
            .order_by("id").reverse()
        comment_order = "1".zfill(2)
        if q_last_comment.count() > 0:
            comment_order = find_comment_order(q_last_comment[0].location)

        file_location = q_take.location
        comment_location = re.sub(r'^(.*)(\.wav|\.mp3)$', r'\1_n'+comment_order+'.'+comment_ext, file_location)

        with open(comment_location, 'w') as temp_file:
            for chunk in comment.chunks():
                temp_file.write(chunk)
        temp_file.close()

        Comment(
            location = comment_location,
            file = q_take,
            user = q_user
        ).save()

        return Response({"location": comment_location}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        instance = self.get_object()
        try:
            os.remove(instance.location)
        except OSError:
            pass
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)

def find_comment_order(location):
    regex = r"_n([0-9]+)\."
    s = re.search(regex, location)
    if regex:
        number = int(s.group(1))
        number += 1
        return str(number).zfill(2)
    return "1".zfill(2)

def find_file_extension(filename):
    return filename[-3:]