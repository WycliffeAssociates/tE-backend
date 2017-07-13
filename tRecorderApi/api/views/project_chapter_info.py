from rest_framework import views, status
from rest_framework.parsers import JSONParser
import json
from api.models import Take
from rest_framework.response import Response
from operator import itemgetter

class ProjectChapterInfoView(views.APIView):
    parser_classes = (JSONParser,)

    def post(self, request):
        data = json.loads(request.body)
        if "version" not in data.keys() or "book" not in data.keys() or "language" not in data.keys(): #or data["book"] == None or data["language"] == None:
            return Response({"response":"notenoughparameters"}, status=403)
        else:
            allTakes = Take.objects.all().values()
            allTakes = allTakes.filter(version=data["version"])
            allTakes = allTakes.filter(book__slug=data["book"])
            allTakes = allTakes.filter(language__slug=data["language"])
            chap = []
            chapters = []
            for take in allTakes:
                if take["chapter"] not in chap:
                    idv = {}
                    idv["chapter"] = take["chapter"]
                    idv["checked_level"] = take["checked_level"]
                    idv["contributors"] = "Jerome"
                    idv["percent_complete"] = 75
                    #mostRecent = ""
                    idv["timestamp"] = take["date_modified"]
                    chap.append(take["chapter"])
                    chapters.append(idv)
                    chapters = sorted(chapters, key = itemgetter('chapter'))
            return Response(chapters, status = 200)
