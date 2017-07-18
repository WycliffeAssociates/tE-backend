from rest_framework import views, status
from rest_framework.parsers import JSONParser
import json
from helpers import getTakesByProject, updateTakesByProject
from rest_framework.response import Response

class UpdateProjectView(views.APIView):
    """This class handles the http POST requests."""
    parser_classes = (JSONParser,)

    def post(self, request):
        data = request.data

        if "filter" not in data or "fields" not in data:
            return Response({"response": "notenoughparameters"}, status=403)

        updated = updateTakesByProject(data)

        return Response({"response": {"rows_affected": updated}}, status=200)