from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Project


class AllProjectsView(APIView):
    parser_classes = (JSONParser,)

    def post(self, request):
        data = request.data
        projects = Project.getProjects(data)
        return Response(projects, status=200)
