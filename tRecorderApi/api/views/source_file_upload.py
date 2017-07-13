from rest_framework import views, status
from rest_framework.parsers import JSONParser, FileUploadParser
import time
import os
import uuid
import subprocess
import json
import shutil
from rest_framework.response import Response
from tinytag import TinyTag
from helpers import getBookByCode, getLanguageByCode, prepareDataToSave

class UploadSourceFileView(views.APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request, filename, format='tr'):
        if request.method == 'POST' and request.data['file']:
            uuid_name = str(time.time()) + str(uuid.uuid4())
            tempFolder = "media" + os.sep + "dump" + os.sep + uuid_name + os.sep
            if not os.path.exists(tempFolder):
                os.makedirs(tempFolder)
                data = request.data['file']
                with open(tempFolder + os.sep + "source.tr", 'w') as temp_file:
                    i = 0
                    # remove first 4 lines from the file which are content-type info
                    # TODO find the better way to get body of the file
                    for line in data:
                        if i > 3:
                            temp_file.write(line)
                        i += 1
        try:
            FNULL = open(os.devnull, 'w')
            subprocess.check_output(
                ['java', '-jar', 'aoh/aoh.jar', '-x', tempFolder + os.sep + "source.tr"],
                stderr=subprocess.STDOUT
            )

            os.remove(tempFolder + os.sep + "source.tr")
            FNULL.close()
            
            bookname = ''
            bookcode = ''
            langname = ''
            langcode = ''

            for root, dirs, files in os.walk(tempFolder):
                for f in files:
                    abpath = os.path.join(root, os.path.basename(f))
                    try:
                        meta = TinyTag.get(abpath)
                    except LookupError:
                        return Response({"response": "badwavefile"}, status=403)

                    if meta and meta.artist:
                        a = meta.artist
                        lastindex = a.rfind("}") + 1
                        substr = a[:lastindex]
                        pls = json.loads(substr)

                        if bookcode != pls['slug']:
                            bookcode = pls['slug']
                            bookname = getBookByCode(bookcode)
                        if langcode != pls['language']:
                            langcode = pls['language']
                            langname = getLanguageByCode(langcode)

                        data = {
                            "langname": langname,
                            "bookname": bookname,
                            "duration": meta.duration
                        }
                        prepareDataToSave(pls, abpath, data, True)
                    else:
                        return Response({"response": "badwavefile"}, status=403)
            return Response({"response": "ok"}, status=200)
        except subprocess.CalledProcessError:
            shutil.rmtree(tempFolder)
            return Response({"response": "badtrfile"}, status=403)
        return Response(status=200)