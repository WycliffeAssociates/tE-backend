from api.file_transfer.FileUtility import FileUtility
from api.file_transfer.TrIt import TrIt
from api.file_transfer.Upload import Upload
from api.file_transfer.ZipIt import ZipIt
from api.models import Take
from django.core.files.storage import FileSystemStorage
from rest_framework import views
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response


class FileUploadView(views.APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request, filename):
        """ Normal upload """
        if request.data["file"]:
            arch_project = ZipIt()
            file_to_upload = request.data["file"]
            fs = FileSystemStorage()
            filename = fs.save(file_to_upload.name, file_to_upload)
            uploaded_file_url = fs.url(filename)
            if filename == "tr":
                arch_project = TrIt()
            up = Upload(arch_project, None, FileUtility())
            resp, stat = up.upload(file_to_upload)
            return Response({"response": resp}, status=stat)
        else:
            return Response({"response": "no file"}, status=200)
