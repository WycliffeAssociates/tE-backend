from rest_framework import views, status
from rest_framework.parsers import JSONParser
import json
from rest_framework.response import Response
from api.models import Take, Chunk

class GetProjectTakesView(views.APIView):
    """This class handles the http POST requests."""
    parser_classes = (JSONParser,)

    def post(self, request):
        data = request.data
        data["is_source"] = False
        
        if "language" in data and "version" in data and "book" in data and "chapter" in data:
            lst = Chunk.getChunksWithTakesByProject(data)
        else:
            return Response({"error": "not_enough_parameters"}, status=400)

        return Response(lst, status=200)