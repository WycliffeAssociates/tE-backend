from api.file_transfer.FileUtility import FileUtility
from api.file_transfer.TrIt import TrIt
from api.file_transfer.Upload import Upload
from api.file_transfer.ZipIt import ZipIt
from api.models import Take
from rest_framework import views
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)

class FileUploadView(views.APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request, filename):
        """ Normal upload """
        if request.data["file"]:
            arch_project = ZipIt()
            file_to_upload = request.data["file"]
            if filename == "tr":
                arch_project = TrIt()
            logger.info("File received with extention: " + filename)
            up = Upload(arch_project, None, FileUtility(), Take)
            resp, stat = up.upload(file_to_upload, filename)
            return Response({"response": resp}, status=stat)
        else:
            logger.e("File upload was empty")
            return Response({"response": "no file"}, status=200)
