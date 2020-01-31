from rest_framework import views
from rest_framework.parsers import JSONParser, FileUploadParser, MultiPartParser
from rest_framework.response import Response
from api.file_transfer.FileUtility import FileUtility
from django.core.files.storage import FileSystemStorage
import logging
import json
import time
import uuid

logger = logging.getLogger(__name__)


class LocalizationView(views.APIView):
    parser_classes = (JSONParser, MultiPartParser,)

    def get(self, request, filename):
        
        json = FileUtility.open_localization_file()

        if(json is not None):
            return Response(json, status=200)
        else:
            return Response({"error":"bad_or_not_exist_json"}, status=400)
        
    def post(self, request, filename):
        
        if request.data["file"]:
            
            uploaded_file = request.data["file"]
            
            fs = FileSystemStorage()
            uuid_name = str(time.time()) + str(uuid.uuid4())
            uploaded_file = fs.save("tmp/" + uuid_name, uploaded_file)
            uploaded_file_url = fs.url(uploaded_file)
            
            try:
                with open(uploaded_file_url) as json_file:
                    localization = json.load(json_file)
                    FileUtility.save_localization_file(localization)
                    return Response({"success": True}, status=200)
            except Exception as e:
                logger.error("Error: ", str(e))

            return Response({"success": False}, status=400)
