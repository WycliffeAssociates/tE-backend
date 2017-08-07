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
            currentChunkSize = int(request.POST.get('resumableCurrentChunkSize'))
            totalSize = int(request.POST.get('resumableTotalSize'))
            totalChunks = int(request.POST.get('resumableTotalChunks'))

            if not self.isChunkUploaded(identifier, filename, chunkNumber):
                chunkPath = self.tempFolder + identifier + "/" + filename + ".part" + chunkNumber
                if not os.path.exists(self.tempFolder + identifier):
                    os.makedirs(self.tempFolder + identifier)

                with open(chunkPath, 'w') as temp_file:
                    for line in upload:
                        temp_file.write(line)

                # check if the size of uploaded chunk is correct
                if os.path.isfile(chunkPath):
                    uplChunkSize = os.path.getsize(chunkPath)
                    print 'Chunk #{}: {} = {}'.format(chunkNumber, currentChunkSize, uplChunkSize)
                    if int(currentChunkSize) != int(uplChunkSize):
                        return Response({"error": "chunk_not_uploaded"}, status=204)

            
            if self.isFileUploadComplete(identifier, filename, totalChunks):
                self.isUploadComplete = True;
                filefolder = self.createFileAndDeleteTmp(identifier, filename)
                filepath = os.path.join(filefolder, filename)
                
                # check if the size of uloaded file is correct
                if os.path.isfile(filepath):
                    uplFileSize = os.path.getsize(filepath)
                    print 'File: {} = {}'.format(totalSize, uplFileSize)
                    
                    if int(totalSize) != int(uplFileSize):
                        shutil.rmtree(filefolder)
                        return Response({"error": "file_is_corrupted"}, status=500)
                    
            return Response(status=200)

    def isChunkUploaded(self, identifier, filename, chunkNumber):
        #print filename + ".part" + str(chunkNumber)
        if os.path.isfile(self.tempFolder + identifier + "/" + filename + ".part" + str(chunkNumber)):
            return True
        
        return False

    def isFileUploadComplete(self, identifier, filename, totalChunks):
        for x in range(totalChunks):
            if not self.isChunkUploaded(identifier, filename, x+1):
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

        uuid_name = str(time.time()) + str(uuid.uuid4())
        filepath = os.path.join(self.tempFolder, uuid_name, filename)
        if not os.path.exists(os.path.join(self.tempFolder, uuid_name)):
            os.makedirs(os.path.join(self.tempFolder, uuid_name))
        
        if self.createFileFromChunks(chunkFiles, filepath):
            self.uploadComplete = True

        self.deleteTempFolder(identifier)

        return os.path.join(self.tempFolder, uuid_name)

    def createFileFromChunks(self, chunkFiles, destFile):
        with open(destFile, "wb") as final_file:
            for chunkFile in chunkFiles:
                try:
                    with open(chunkFile, "rb") as chunk:
                        final_file.write(chunk.read())
                except:
                    pass
                
        return os.path.isfile(destFile)

    def deleteTempFolder(self, identifier):
        try:
            shutil.rmtree(self.tempFolder + identifier)
        except:
            pass

    def sort_nicely(self, l):
        """ Sort the given list in the way that humans expect."""
        convert = lambda text: int(text) if text.isdigit() else text
        alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
        l.sort( key=alphanum_key )


    def get(self, request, filename, format='zip'):
        identifier = request.GET.get('resumableIdentifier')
        filename = request.GET.get('resumableFilename')
        chunkNumber = int(request.GET.get('resumableChunkNumber'))

        if self.isChunkUploaded(identifier, filename, chunkNumber):
            return Response(status=200)

        return Response(status=204)