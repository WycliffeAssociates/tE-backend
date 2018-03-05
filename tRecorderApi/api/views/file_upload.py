from django.core.files.storage import FileSystemStorage
from rest_framework import views
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response

from api.file_transfer.FileUtility import FileUtility
from api.file_transfer.TrIt import TrIt
from api.file_transfer.Upload import Upload
from api.file_transfer.ZipIt import ZipIt
from api.models import Take
from rest_framework import views
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
import logging
from raven.contrib.django.raven_compat.models import client

# Get an instance of a logger
logger = logging.getLogger(__name__)


class FileUploadView(views.APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request, filename):
        logger.info("in upload view!")
        """ Normal upload """
        if request.data["file"]:
            arch_project = ZipIt()
            file_to_upload = request.data["file"]
            fs = FileSystemStorage()
            filename_to_upload = fs.save(file_to_upload.name, file_to_upload)
            uploaded_file_url = fs.url(filename_to_upload)
            if filename == "tr":
                arch_project = TrIt()
            up = Upload(arch_project, None, FileUtility())
            up.upload(uploaded_file_url)
            return Response({"response": "processing"}, status=202)
        else:
            return Response({"response": "no file"}, status=200)
