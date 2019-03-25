import logging

from django.core.files.storage import FileSystemStorage
from rest_framework import views
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from api.file_transfer.FileUtility import FileUtility
from api.file_transfer.TrIt import TrIt
from api.file_transfer.Upload import Upload
from api.file_transfer.ZipIt import ZipIt
from api.models import User

# Get an instance of a logger
logger = logging.getLogger(__name__)


class FileUploadView(views.APIView):
    parser_classes = (FileUploadParser,)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def post(self, request, filename):
        """ Normal upload """
        if request.data["file"]:
            arch_project = ZipIt()
            file_to_upload = request.data["file"]

            fs = FileSystemStorage()
            filename_to_upload = fs.save("tmp/" + file_to_upload.name, file_to_upload)
            uploaded_file_url = fs.url(filename_to_upload)

            if filename == "tr":
                arch_project = TrIt()
            up = Upload(arch_project, None, FileUtility())

            user_data = {}
            file_name = "unknown_file_name"
            
            if "HTTP_TR_FILE_NAME" in request.META:
                file_name = request.META["HTTP_TR_FILE_NAME"]

            if request.user.is_anonymous:
                user_hash = "unknown_user_hash"
                
                if "HTTP_TR_USER_HASH" in request.META:
                    user_hash = request.META["HTTP_TR_USER_HASH"]
                
                user = User.objects.filter(icon_hash=user_hash).first()
                if user:
                    user_data["icon_hash"] = user.icon_hash
                    user_data["name_audio"] = user.name_audio
                else:
                    user_data["icon_hash"] = user_hash
                    user_data["name_audio"] = None
            else:
                user_data["icon_hash"] = request.user.icon_hash
                user_data["name_audio"] = request.user.name_audio

            task_id = up.upload(uploaded_file_url, user_data, file_name)
            return Response({"response": "processing", "task_id": task_id}, status=202)
        else:
            return Response({"response": "no file"}, status=200)
