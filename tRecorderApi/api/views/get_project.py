from rest_framework import views, status
from rest_framework.parsers import JSONParser
import json
from helpers import getTakesByProject
from rest_framework.response import Response

class GetProjectView(views.APIView):
    """This class handles the http POST requests."""
    parser_classes = (JSONParser,)

    def post(self, request):
        data = json.loads(request.body)
        data["is_source"] = False
        lst = getTakesByProject(data)

        return Response(lst, status=200)