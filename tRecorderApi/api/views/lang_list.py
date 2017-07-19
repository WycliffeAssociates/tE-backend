from rest_framework import views, status
from rest_framework.parsers import JSONParser
import json
from api.models import Take, Language
from rest_framework.response import Response
from operator import itemgetter

class getLangsView(views.APIView):
    parser_classes = (JSONParser,)

    def post(self, request):
        data = json.loads(request.body)
        allTakes = Take.objects.all().values()
        allTakes = allTakes.filter(is_source = False)
        langs = []
        for take in allTakes:
            lang_uage = Language.objects.filter(id = take["language_id"]).values()
            lang_uage = list(lang_uage)
            if lang_uage[0] not in langs:
                langs.append(lang_uage[0])
        return Response(langs, status = 200)
