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

        if "project" not in data:
            if 'language' not in data or 'version' not in data or "book" not in data:
                return Response({"error": "not_enough_parameters"}, status=400)
        if "chapter" not in data:
            return Response({"error": "not_enough_parameters"}, status=400)

        # parameters in the browser url not in the database field form, so needed to tweak

        data['language_slug'] = data.pop('language')
        data['book_slug'] = data.pop('book')
        data['chapter_number'] = data.pop('chapter')
        data['version_slug'] = data.pop('version')

        lst = Chunk.with_takes_by_project(data)

        return Response(lst, status=200)
