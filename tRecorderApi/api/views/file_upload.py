from api.models import Book, Language, Take
from rest_framework import views
from rest_framework.parsers import FileUploadParser
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from api.file_transfer.Upload import Upload
from api.file_transfer.ZipIt import ZipIt
from api.file_transfer.TrIt import TrIt
from api.file_transfer.FileUtility import FileUtility


class FileUploadView(views.APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, filename):
        """ Normal upload """
        if request.data["upload"]:
            arch_project = ZipIt()
            file_to_upload = request.data["upload"]
            ext = file_to_upload.name.rsplit('.', 1)[-1]  # get file extension
            if ext == "tr":
                arch_project = TrIt()
            up = Upload(arch_project, None, FileUtility(), Take)
            resp, stat = up.upload(file_to_upload, ext)
            return Response({"response": resp}, status=stat)
        else:
            return Response({"response": "no file"}, status=200)
