from rest_framework import views, status
from rest_framework.parsers import MultiPartParser
import time
import os
import uuid
import subprocess
import json
import shutil
from rest_framework.response import Response
from tinytag import TinyTag
from helpers import highPassFilter, getRelativePath
from api.models import Language, Book, Take
from django.conf import settings

class UploadSourceFileView(views.APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, filename, format='tr'):
        if request.method == 'POST' and request.data['upload']:
            # TODO remove this functionality
            
            response = {}
            uuid_name = str(time.time()) + str(uuid.uuid4())
            tempFolder = os.path.join(settings.BASE_DIR, "media/dump/" + uuid_name)
            if not os.path.exists(tempFolder):
                os.makedirs(tempFolder)
                data = request.data['upload']
                with open(os.path.join(tempFolder, "source.tr"), 'w') as temp_file:
                    for line in data:
                        temp_file.write(line)
        try:
            FNULL = open(os.devnull, 'w')
            subprocess.check_output(
                ['java', '-jar', os.path.join(settings.BASE_DIR, 'aoh/aoh.jar'), '-x', tempFolder + "/source.tr"],
                stderr=subprocess.STDOUT
            )

            os.remove(os.path.join(tempFolder, "source.tr"))
            FNULL.close()
            
            bookname = ''
            bookcode = ''
            langname = ''
            langcode = ''

            for root, dirs, files in os.walk(tempFolder):
                for f in files:
                    abpath = os.path.join(root, os.path.basename(f))
                    relpath = getRelativePath(abpath)
                    meta = TinyTag.get(abpath)

                    if meta and meta.artist:
                        a = meta.artist
                        lastindex = a.rfind("}") + 1
                        substr = a[:lastindex]
                        pls = json.loads(substr)

                        if bookcode != pls['slug']:
                            bookcode = pls['slug']
                            bookname = Book.getBookByCode(bookcode)
                        if langcode != pls['language']:
                            langcode = pls['language']
                            langname = Language.getLanguageByCode(langcode)

                        data = {
                            "langname": langname,
                            "bookname": bookname,
                            "duration": meta.duration
                        }

                        #highPassFilter(abpath)
                        saved = Take.prepareDataToSave(pls, relpath, data, True)
                        if "language" in saved and "language" not in response:
                            response["language"] = saved["language"]
                        if "book" in saved and "book" not in response:
                            response["book"] = saved["book"]
                    else:
                        return Response({"error": "bad_wave_file"}, status=400)
            return Response(response, status=200)
        except Exception as e:
            shutil.rmtree(tempFolder)
            return Response({"error": str(e)}, status=400)


            # code flow

    """
def post(request):

    // dealing with file system   
    1. Create a temporary folder path 
    2. check if the path exists
    3. if it does not exist make direction
    4. open the file in the temporary direction
    5. open os.devnull -- (not sure what this is doing)
    6. create a path
    7. remove file path using os.remove 
    8. loop in the temporary folder
    9. get absolute and relative path

    
    // code flow
    1.0 check if it is a post request if not return and exception error
    1.1 create dictionary response 
    1. create unique name uuid_name
    2. create a temporary file path
    3. it the path does not exist we create a direction
    4. get the data and open it in the temp folder
    5. FNUll = open os.devnull -- (not sure what this is doing)
    6. check the output file
    7. remove path with the temporary folder 
    8. close FNULL 
    9. loop through the files, 
    10. get absolute path
    11. get relative path
    12. get metadata
    13. if there is metadata and meta artist split data by } if not return response error bad wave file
    14. create a json object
    15. from the json object create bookcode
    16. get the bookcode from book
    17. from json object create language code
    18. get the language code from book
    19. create a dictionary with language name book name and duration
    20. saved = pass the json object, the relative path, the dictionary and a True to a function 
        in Take called prepareDataToSave
    21. check if language is in saved and not in response: if this is true response["language"] = saved["language"]
    22. check if book is in saved and not in response: if this is true response["book"] = saved["book"]     
    23. return (response, status= 200)
    




    """