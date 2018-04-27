import logging

from django.core.files.storage import FileSystemStorage
from rest_framework import views
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.response import Response

from api.file_transfer.FileUtility import FileUtility
from api.file_transfer.TrIt import TrIt
from api.file_transfer.Upload import Upload
from api.file_transfer.ZipIt import ZipIt

# Get an instance of a logger
logger = logging.getLogger(__name__)


class FileUploadView(views.APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, filename):

        """ Normal upload """
        if request.data["file"]:
            arch_project = ZipIt()
            file_to_upload = request.data["file"]
            langslug = ""
            langname = ""
            bookslug = ""
            bookname = ""

            if "langslug" in request.data:
                langslug = request.data["langslug"]
            if "langname" in request.data:
                langname = request.data["langname"]
            if "bookslug" in request.data:
                bookslug = request.data["bookslug"]
            if "bookname" in request.data:
                bookname = request.data["bookname"]

            fs = FileSystemStorage()
            filename_to_upload = fs.save("tmp/" + file_to_upload.name, file_to_upload)
            uploaded_file_url = fs.url(filename_to_upload)

            if filename == "tr":
                arch_project = TrIt()
            up = Upload(arch_project, None, FileUtility())
            task_id = up.upload(uploaded_file_url, langslug, langname, bookslug, bookname)
            return Response({"response": "processing", "task_id": task_id}, status=202)
        else:
            return Response({"response": "no file"}, status=200)
