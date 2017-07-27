from rest_framework import views, status
from rest_framework.parsers import JSONParser
import time
import uuid
import os
import shutil
import pydub
import json
import subprocess
from rest_framework.response import Response
from django.http import HttpResponse
from django.core import files
from rest_framework.parsers import JSONParser, FileUploadParser
from tinytag import TinyTag
import urllib2
import pickle
from api.models import Take, Chunk


class SourceFileView(views.APIView):
    parser_classes = (JSONParser,)

    def post(self, request):
        data = request.data

        if "project" not in data:
            if 'language' not in data or 'version' not in data \
                or "book" not in data:
                return Response({"error", "not_enough_parameters"}, status=400)

        new_data = {}

        if "project" in data:
            new_data["project"] = data["project"]
        else:
            new_data["language"] = data["language"]
            new_data["version"] = data["version"]
            new_data["book"] = data["book"]
        new_data["is_publish"] = True
        
        project = Chunk.getChunksWithTakesByProject(new_data)
        if len(project["chunks"]) > 0:
            uuid_name = str(time.time()) + str(uuid.uuid4())
            root_folder = 'media/tmp/' + uuid_name
            filename = project['language']["slug"]+'_'+project['project']['version']+'_'+project['book']['slug']
            project_folder = root_folder+'/'+project['language']["slug"]+'/'+project['project']['version']+'/'+project['book']['slug']
            
            try:
                for chunk in project["chunks"]:
                    for take in chunk["takes"]:
                        chapter_folder = project_folder + '/' + str(
                            project['chapter']['number']).zfill(2)
                        if not os.path.exists(chapter_folder):
                            os.makedirs(chapter_folder)
                        shutil.copy2(take['take']['location'], chapter_folder)
                        file_name = os.path.basename(take['take']['location'])
                        file_path = chapter_folder + '/' + file_name
                        
                        if file_path.endswith('.wav'):
                            file_path_mp3 = file_path.replace('.wav', '.mp3')

                            meta = {
                                "anthology": project['project']["anthology"],
                                "language": project["language"]["slug"],
                                "version": project['project']["version"],
                                "slug": project['book']["slug"],
                                "book_number": str(project['book']["booknum"]).zfill(2),
                                "mode": project['project']["mode"],
                                "chapter": str(project["chapter"]['number']).zfill(2),
                                "startv": chunk["startv"],
                                "endv": chunk["endv"],
                                "markers": take['take']["markers"]
                            }

                            sound = pydub.AudioSegment.from_wav(file_path)
                            sound.export(file_path_mp3, format='mp3', tags={'artist': json.dumps(meta)})
                            os.remove(file_path)

                FNULL = open(os.devnull, 'w') 
                subprocess.call(['java', '-jar', 'aoh/aoh.jar', '-c', '-tr', root_folder],
                                stdout=FNULL, stderr=subprocess.STDOUT)
                FNULL.close()
                os.rename(root_folder+'.tr', 
                    'media/tmp/'+filename+'.tr')
                shutil.rmtree(root_folder)
            except Exception as e:
                return Response({"error": str(e)}, status=400)
        else:
            return Response({"response": "no_source_files"}, status=400)

        with open('media/tmp/'+filename+'.tr', 'rb') as source_file:
            response = HttpResponse(files.File(source_file), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="%s"' % (
            filename+'.tr')
        
        return response

