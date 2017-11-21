from rest_framework import views, status
from rest_framework.parsers import JSONParser
import json
from .helpers import getFileName, md5Hash
from rest_framework.response import Response
from api.models import Chunk

class ExcludeFilesView(views.APIView):
    parser_classes = (JSONParser,)

    def post(self, request):
        files_to_exclude = {}
        data = request.data
        project = Chunk.getChunksWithTakesByProject(data)
        for chunk in project["chunks"]:
            for take in chunk['takes']:
                location = take['take']['location']
                files_to_exclude[getFileName(location)] = md5Hash(location)
        return Response(files_to_exclude, status=200)