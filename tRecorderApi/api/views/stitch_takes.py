from pydub import AudioSegment
from rest_framework import views, status
from rest_framework.parsers import JSONParser
from api.models import Take, Language, Book, User, Comment, Project
import json
from rest_framework.response import Response
import os
from django.conf import settings
from helpers import getRelativePath

class SourceStitchView(views.APIView):
    parser_classes = (JSONParser,)
    def post(self, request):
        data = request.data
        if "language" in data and "version" in data and "book" in data and "chapter" in data:
            chunks = Take.stitchSource(data)
            #chunks = list(chunks)
            chunks = sorted(chunks, key = lambda x: x.startv)
            loclst = []
            for chunk in chunks:
                takes = chunk.take_set.all()
                for take in takes:
                    # do not enclude takes that are not published
                    if take.is_publish != True:
                        continue
                
                    loclst.append(os.path.join(settings.BASE_DIR, take.location))

            if len(loclst) > 0:
                stitchedSource = AudioSegment.from_mp3(loclst[0])
                loclst.pop(0)
                for item in loclst:
                    sound1 = stitchedSource
                    sound2 = AudioSegment.from_mp3(item)
                    stitchedSource = sound1 + sound2
                stitch_folder = os.path.join(settings.BASE_DIR, 'media/source')
                if not os.path.exists(stitch_folder):
                    os.makedirs(stitch_folder)
                project_name = data["language"] + "_" + data["version"] + "_" + data["book"] + "_" + str(data["chapter"])
                stitchedSource.export(stitch_folder+"/"+project_name+".mp3", format="mp3")
            else:
                return Response({"error": "no_published_takes"}, status=400)
        else:
            return Response({"error": "not_enough_parameters"}, status=400)
        
        return Response({"location": getRelativePath(stitch_folder+"/"+project_name+".mp3")}, status = 200)
