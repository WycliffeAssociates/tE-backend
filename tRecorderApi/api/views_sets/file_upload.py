from rest_framework import views, status
from rest_framework.parsers import JSONParser, FileUploadParser
import time
import uuid
import zipfile
import os
from tinytag import TinyTag
from rest_framework.response import Response
import json
from helpers import getBookByCode, getLanguageByCode, prepareDataToSave

class FileUploadView(views.APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request, filename, format='zip'):
        if request.method == 'POST' and request.data['file']:
            uuid_name = str(time.time()) + str(uuid.uuid4())
            upload = request.data["file"]

            # unzip files
            try:
                zip = zipfile.ZipFile(upload)
                folder_name = 'media/dump/' + uuid_name

                zip.extractall(folder_name)
                zip.close()

                # extract metadata / get the apsolute path to the file to be stored

                # Cache language and book to re-use later
                bookname = ''
                bookcode = ''
                langname = ''
                langcode = ''

                for root, dirs, files in os.walk(folder_name):
                    for f in files:
                        abpath = os.path.join(root, os.path.basename(f))
                        # abpath = os.path.abspath(os.path.join(root, f))
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
                            prepareDataToSave(pls, abpath, data)
                        else:
                            return Response({"response": "badwavefile"}, status=403)
                return Response({"response": "ok"}, status=200)

            except zipfile.BadZipfile:
                return Response({"response": "badzipfile"}, status=403)
        else:
            return Response(status=404)