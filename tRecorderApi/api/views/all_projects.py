from rest_framework import views, status
from rest_framework.parsers import JSONParser
from api.models import Take, Language, Book, User, Comment
import json
from rest_framework.response import Response
from api.models import Project


class AllProjectsView(views.APIView):
    parser_classes = (JSONParser,)

    @staticmethod
    def post(request):
        data = request.data

        projects = Project.getProjects(data)

        return Response(projects, status=200)
