from rest_framework import views, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from ..models import Project


class GetProjectsView(views.APIView):
    parser_classes = (JSONParser,)

    @staticmethod
    def post(request):
        data = request.data
        project_filter = {}

        if data["language"] is not None:
            project_filter["language__slug"] = data["language"]
        if data["version"] is not None:
            project_filter["version__slug"] = data["version"]
        if data["book"] is not None:
            project_filter["book__slug"] = data["book"]
        if data["published"] is not None:
            project_filter["published"] = data["published"]
        if data["anthology"] is not None:
            project_filter["anthology__slug"] = data["anthology"]

        # filter projects based on the project being requested
        filtered_projects = Project.objects.filter(**project_filter)

        projects = Project.get_projects(filtered_projects)
        return Response(projects, status=200)
