from pydub import AudioSegment
from rest_framework import views, status
from rest_framework.parsers import JSONParser
from api.models import Take, Language, Book, User, Comment, Project
import json
from rest_framework.response import Response


class SourceStitchView(views.APIView):
    parser_classes = (JSONParser,)
    def post(self, request):
        data = request.data
        data["is_source"] = True
        lst = Take.stitchSource(data)

        return Response(lst, status = 200)
