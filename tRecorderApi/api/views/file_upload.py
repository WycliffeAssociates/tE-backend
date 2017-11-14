from api.models import Book, Language, Take
from rest_framework import views
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from api.file_transfer.Upload import Upload
from api.file_transfer.ZipIt import ZipIt
from api.file_transfer.TrIt import TrIt
from api.file_transfer.FileUtility import FileUtility


class FileUploadView(views.APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request, filename, format='zip'):
        """ Normal upload """
        arch_project = ZipIt()
        file_to_upload = request.data["file"]
        if file_to_upload.name == "tr":        #check if it is a .tr source file
            arch_project = TrIt()

        up = Upload(arch_project, None, FileUtility(), Take)
        resp, stat = up.upload(file_to_upload)
        return Response({"response": resp}, status=stat)
