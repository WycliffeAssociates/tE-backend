from rest_framework import views, status
from rest_framework.parsers import JSONParser
import time
import os
import uuid
import shutil
from tinytag import TinyTag
from pydub import AudioSegment
import zipfile
from rest_framework.response import Response
from django.http import HttpResponse
from api.models import Chunk

class ProjectZipFilesView(views.APIView):
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
        #new_data["is_publish"] = True

        project = Chunk.getChunksWithTakesByProject(new_data)
        
        if len(project["chunks"]) > 0:
            filesInZip = []
            uuid_name = str(time.time()) + str(uuid.uuid4())
            root_folder = 'media/export/' + uuid_name
            chapter_folder = ""
            project_name = project['language']["slug"] + \
                "_" + project['project']['version'] + \
                "_" + project['book']['slug']

            if not os.path.exists(root_folder):
                os.makedirs(root_folder)

            # create list for locations
            locations = []
            for chunk in project["chunks"]:
                for take in chunk['takes']:
                    chapter_folder = root_folder + os.sep + project['language']["slug"] + \
                        os.sep + project['project']['version'] + \
                        os.sep + project['book']['slug'] + \
                        os.sep + str(project['chapter']['number'])

                    if not os.path.exists(chapter_folder):
                        os.makedirs(chapter_folder)

                    loc = {}
                    loc["src"] = take["take"]["location"]
                    loc["dst"] = chapter_folder
                    locations.append(loc)

            # use shutil to copy the wav files to a new folder
            for loc in locations:
                shutil.copy2(loc["src"], loc["dst"])

            # process of renaming/converting to mp3
            for subdir, dirs, files in os.walk(root_folder):
                for file in files:
                    # store the absolute path which is is it's subdir and where the os step is
                    filePath = subdir + os.sep + file

                    if filePath.endswith(".wav"):
                        # Add to array so it can be added to the archive
                        sound = AudioSegment.from_wav(filePath)
                        filename = filePath.replace(".wav", ".mp3")
                        sound.export(filename, format="mp3")
                        filesInZip.append(filename)
                    else:
                        filesInZip.append(filePath)

            # Creating zip file
            with zipfile.ZipFile('media/export/' + project_name + '.zip', 'w') as zipped_f:
                for members in filesInZip:
                    zipped_f.write(members, members.replace(root_folder,""))

            # delete the newly created wave and mp3 files
            shutil.rmtree(root_folder)

            with open('media/export/' + project_name + '.zip', 'rb') as zip_file:
                response = HttpResponse(zip_file, content_type='application/zip')
                response['Content-Disposition'] = 'attachment; filename='+project_name+'.zip'

            return response
        else:
            return Response({"error":"no_files"}, status=400)