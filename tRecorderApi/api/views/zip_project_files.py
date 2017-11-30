from api.file_transfer.ArchiveIt import ArchiveIt
from api.file_transfer.AudioUtility import AudioUtility
from api.file_transfer.Download import Download
from api.file_transfer.FileUtility import FileUtility
from api.models import Chunk
from api.models import Version
import os
import shutil
import time
import uuid
import zipfile
from api.models import Chunk
from django.conf import settings
from .helpers import getRelativePath
from pydub import AudioSegment
from rest_framework import views
from rest_framework.parsers import JSONParser
from rest_framework.response import Response


class ZipProjectFiles(views.APIView):
    parser_classes = (JSONParser,)

    def post(self, request):
        data = request.data
        if "version_slug" not in data and "book_slug" not in data and "language_slug" not in data:
                return Response({"error", "not_enough_parameters"}, status=400)
        else:
            chunk_list = Chunk.with_takes_by_project(data)
            if len(chunk_list['chunks']) > 0:
                language_slug = chunk_list['language']["slug"]
                version_slug = Version.slug_by_version_id(chunk_list['project']['version'])
                book_slug = chunk_list['book']['slug']

                project_name = language_slug + "_" + version_slug + "_" + book_slug

                zip_it = Download(ArchiveIt(), AudioUtility(), FileUtility())

                root_dir = zip_it.file_utility.root_dir(['media', 'export'])

                location_list = self.location_list(root_dir, chunk_list, zip_it.file_utility.create_path,
                                                   zip_it.file_utility.take_location)

                zipped_file_location = zip_it.download(project_name, location_list, root_dir)
                return Response({"location": zip_it.file_utility.relative_path(zipped_file_location)}, status=200)
            else:
                return Response({"error": "no_files"}, status=400)

    @staticmethod
    def location_list(root_dir, chunk_list, chapter_dir, take_location):
        chapter_directory = ""
        locations = []
        for chunk in chunk_list["chunks"]:
            for take in chunk['takes']:
                lang = chunk_list['language']["slug"]
                version = Version.slug_by_version_id(chunk_list['project']['version'])
                book = chunk_list['book']['slug']
                number = str(chunk_list['chapter']['number'])
                location = {}
                location["src"] = take_location(take["take"]["location"])
                location["dst"] = chapter_dir(root_dir, lang, version, book, str(number))
                locations.append(location)
        return locations

 # code flow
"""
//dealing with data received
1.Check project is in the data
2.If project is not in data check language,version,book is not in data,then return not enough parameter
3.Create an empty dictionary
4.Check if project is in data
5.if project is in data assign it to dictionary created,else
6.check if language,book,version is in data
7.If language,book,version is in data assign them to the created dictionary
//dealing with database
8.Fetch project(which is array of chunks with array of takes),database query
9.Check if project exist
//dealing with file system
10.If porject exists,construct project_path
11.Create directory for project(project_path) if it doesn't exist
12.Loop through Chunks and create chapter_path
13.Loop through takes in chunk
14.Create array of takes location(source and destination)
15.Copy takes to destination from source location
//data manupulation and informing
16.Converts moved .wav file to .mp3
17.Zip the files and send response with location of files,else
18.Send Response with status 400
"""