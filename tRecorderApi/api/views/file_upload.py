from rest_framework import views, status
from rest_framework.parsers import JSONParser, FileUploadParser
import time
import uuid
import zipfile
import os
from tinytag import TinyTag
from rest_framework.response import Response
import json
from helpers import highPassFilter, getRelativePath
from api.models import Book, Language, Take
from django.conf import settings
import shutil


class FileUploadView(views.APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request, filename, format='zip'):
        """ Normal upload """
        if request.method == 'POST' and request.data['file']:
            #create a unique name
            uuid_name = str(time.time()) + str(uuid.uuid4())
            #get the file
            upload = request.data["file"]

            # unzip files
            try:
                #read the object
                zip = zipfile.ZipFile(upload)
                #create a folder
                folder_name = os.path.join(settings.BASE_DIR, 'media/dump/' + uuid_name)
                zip.extractall(folder_name)
                zip.close()

                # extract metadata / get the apsolute path to the file to be stored

                # Cache language and book to re-use later
                bookname = ''
                bookcode = ''
                langname = ''
                langcode = ''

                is_empty_zip = True # for testing if zip file is empty

                for root, dirs, files in os.walk(folder_name):
                    for f in files:
                        is_empty_zip = False
                        abpath = os.path.join(root, os.path.basename(f))
                        relpath = getRelativePath(abpath)
                        try:
                            meta = TinyTag.get(abpath)
                        except LookupError as e:
                            return Response({"error": "bad_wave_file"}, status=400)
                        
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
                            
                            highPassFilter(abpath)
                            Take.prepareDataToSave(pls, relpath, data)
                        else:
                            return Response({"error": "bad_wave_file"}, status=400)
                
                if is_empty_zip:
                    return Response({"error": "bad_zip_file"}, status=400)
                return Response({"response": "ok"}, status=200)

            except zipfile.BadZipfile:
                return Response({"error": "bad_zip_file"}, status=400)
        else:
            return Response(status=404)

    @staticmethod
    def processFile(folderPath, filePath):
        """ File processor for resumable upload """
        # unzip files
        try:
            location = os.path.join(folderPath, filePath)
            uuid_name = str(time.time()) + str(uuid.uuid4())
            zip = zipfile.ZipFile(location)
            folder_name = os.path.join(settings.BASE_DIR, 'media/dump/' + uuid_name)

            zip.extractall(folder_name)
            zip.close()
            shutil.rmtree(folderPath, ignore_errors=True)

            # Cache language and book to re-use later
            bookname = ''
            bookcode = ''
            langname = ''
            langcode = ''

            is_empty_zip = True # for testing if zip file is empty

            for root, dirs, files in os.walk(folder_name):
                for f in files:
                    is_empty_zip = False
                    abpath = os.path.join(root, os.path.basename(f))
                    relpath = getRelativePath(abpath)
                    try:
                        meta = TinyTag.get(abpath)
                    except LookupError as e:
                        return {"error": "bad_wave_file"}
                    
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
                        
                        highPassFilter(abpath)
                        Take.prepareDataToSave(pls, relpath, data)
                    else:
                        return {"error": "bad_wave_file"}
            
            if is_empty_zip:
                return {"error": "bad_zip_file"}
            
            return {"response": "ok"}

        except zipfile.BadZipfile:
            return {"error": "bad_zip_file"}

    # code flow
    """
def post(request):
    //dealing with data received
    1. Extract the zip file with the library zip, if it is not a zip file catches an error.
    2. Check if there is meta data and if there is artist field in file metadata.
       if there is not return an error.
    3. Split the file and create a json object for each file. 
    4. Get book code and language code from json object.
    5. create a dictionary and pass it to a function in take model.
       
    // dealing with file system   
    1. Create a folder path 
    2. loop in the folder with the extracted files
    3. Get absolute and relative path
    
    
    // code flow
    1. create unique name uuid_name
    2. get the uploaded file
    3. read the zip file if not zip file returns bad file
    4. create folder in the system 
    5. extract the zip file and close the zip library
    6. create a boolean to check if the file is empty
    7. loop through the file directory extracted
    8. loop through the files, if there are files set boolean empty files to false and loop
       if there are not files return bad zip file
    9. get absolute path
    10. get relative path
    11. try to get metadata if there is an exception return bad wave file
    12. if there is metadata and meta artist split data by } 
    13. create a json object
    14. from the json object create bookcode
    15. get the bookcode from book
    16. from json object create language code
    17. get the language code from book
    18. create a dictionary with language name book name and duration
    19. apply high pass filter using absolute path
    20. pass the json object, the relative path and dictionary to a function 
        in Take called prepareDataToSave
    21. return response ok status 400      

    
    
def processFile(folderPath, filePath): 
    //dealing with data received
    1. Extract the zip file with the library zip, if it is not a zip file catches an error.
    3. Erase the exiting path folder
    2. Check if there is meta data and if there is artist field in file metadata.
       if there is not return an error.
    3. Split the file and create a json object for each file. 
    4. Get book code and language code from json object.
    5. create a dictionary and pass it to a function in take model.
    
    // dealing with file system   
    1. Create location path 
    2. Create a folder path   
    3. loop in the created folder path 
    4. Get absolute and realtive path
    
    
    // code flow    
    1. get location path by using the arguments passed as folderPath and filePath
    2. create unique name
    3. read the zip file if not zip file returns bad file
    4. create folder in the system 
    5. extract the zip file and close the zip library
    6. use function from library shutil.rmtree(folderPath) to remove the folder tree ???
    7. create a boolean to check if the file is empty
    8. loop through the file directory extracted
    9. loop through the files, if there are files set boolean empty files to false and loop
       if there are not files return bad zip file
    10. get absolute path
    11. get relative path
    12. try to get metadata if there is an exception return bad wave file
    13. if there is metadata and meta artist split data by } 
    14. create a json object
    15. from the json object create bookcode
    16. get the bookcode from book
    17. from json object create language code
    18. get the language code from book
    19. create a dictionary with language name book name and duration
    20. apply high pass filter using absolute path
    21. pass the json object, the relative path and dictionary to a function 
        in Take called prepareDataToSave
    21. return response ok status 400 
      
    """