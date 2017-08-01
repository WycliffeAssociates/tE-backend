from rest_framework import views, status
from rest_framework.parsers import MultiPartParser
import time
import uuid
import zipfile
import os
import shutil
from tinytag import TinyTag
from rest_framework.response import Response
import json
import re
from helpers import highPassFilter
from api.models import Book, Language, Take
from django.conf import settings

class ResumableFileUploadView(views.APIView):
    parser_classes = (MultiPartParser,)

    tempFolder = os.path.join(settings.BASE_DIR, "media/tmp/")
    isUploadComplete = False

    def post(self, request, filename, format='zip'):
        if request.method == 'POST' and request.data['file']:
            upload = request.data["file"]
            identifier = request.POST.get('resumableIdentifier')
            filename = request.POST.get('resumableFilename')
            chunkNumber = request.POST.get('resumableChunkNumber')
            chunkSize = int(request.POST.get('resumableChunkSize'))
            totalSize = int(request.POST.get('resumableTotalSize'))

            if not self.isChunkUploaded(identifier, filename, chunkNumber):
                if not os.path.exists(self.tempFolder + identifier):
                    os.makedirs(self.tempFolder + identifier)

                with open(self.tempFolder + identifier + "/" + filename + ".part" + chunkNumber, 'w') as temp_file:
                    for line in upload:
                        temp_file.write(line)
            
            if self.isFileUploadComplete(identifier, filename, chunkSize, totalSize):
                self.isUploadComplete = True;
                self.createFileAndDeleteTmp(identifier, filename)
                return Response({"response":"ok"}, status=200)

            return Response(status=200)

    def get(self, request, filename, format='zip'):
        identifier = request.GET.get('resumableIdentifier')
        filename = request.GET.get('resumableFilename')
        chunkNumber = int(request.GET.get('resumableChunkNumber'))

        if self.isChunkUploaded(identifier, filename, chunkNumber):
            return Response(status=200)

        return Response(status=404)

    def isChunkUploaded(self, identifier, filename, chunkNumber):
        if os.path.isfile(self.tempFolder + identifier + "/" + filename + ".part" + str(chunkNumber)):
            return True
        
        return False

    def isFileUploadComplete(self, identifier, filename, chunkSize, totalSize):
        if chunkSize <= 0:
            return False
        
        remainder = totalSize % chunkSize
        if remainder != 0:
            remainder = 1 
        numOfChunks = (totalSize / chunkSize) + remainder
        
        for x in range(1, numOfChunks):
            if not self.isChunkUploaded(identifier, filename, x):
                return False

        return True;

    def createFileAndDeleteTmp(self, identifier, filename):
        folder = self.tempFolder + identifier
        chunkFiles = []
        for root, dirs, files in os.walk(folder):
            for f in files:
                abpath = os.path.join(root, os.path.basename(f))
                chunkFiles.append(abpath)
        
        self.sort_nicely(chunkFiles)

        filepath = self.tempFolder + filename
        if self.createFileFromChunks(chunkFiles, filepath):
            shutil.rmtree(folder)
            self.uploadComplete = True

    def createFileFromChunks(self, chunkFiles, destFile):
        with open(destFile, "wb") as final_file:
            for chunkFile in chunkFiles:
                with open(chunkFile, "rb") as chunk:
                    final_file.write(chunk.read())

        return os.path.isfile(destFile)

    def sort_nicely(self, l):
        """ Sort the given list in the way that humans expect."""
        convert = lambda text: int(text) if text.isdigit() else text
        alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
        l.sort( key=alphanum_key )