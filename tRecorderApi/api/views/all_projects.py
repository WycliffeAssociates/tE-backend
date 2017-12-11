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

        if not data:
            all_projects = Project.objects.all()
            projects = Project.get_projects(all_projects)

        else:
            if "language" in data:
                project_filter["language__slug"] = data["language"]
            if "version" in data:
                project_filter["version__slug"] = data["version"]
            if "book" in data:
                project_filter["book__slug"] = data["book"]
            if "published" in data:
                project_filter["published"] = data["published"]
            if "anthology" in data:
                project_filter["anthology__slug"] = data["anthology"]

            # filter projects based on the project being requested
            filtered_projects = Project.objects.filter(**project_filter)

            projects = Project.get_projects(filtered_projects)

        return Response(projects, status=200)
