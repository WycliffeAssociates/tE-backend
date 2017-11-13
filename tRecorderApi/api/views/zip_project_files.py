import datetime
import json
import os

from api.file_transfer.AudioUtility import AudioUtility
from api.file_transfer.Download import Download
from api.file_transfer.FileUtility import FileUtility
from api.file_transfer.ZipIt import ZipIt
from api.models import Chunk
from django.conf import settings
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView


class ZipProjectFiles(APIView):
    parser_classes = (JSONParser,)

    def post(self, request):
        data = request.data
        # project_to_find = self.chunk_list(data)
        project_to_find = {
            "language": "en-x-demo2",
            "version": "ulb",
            "book": "mrk"
        }
        chunk_list = self.fake_data()
        if len(chunk_list['chunks']) > 0:
            zip_it = Download(ZipIt(), AudioUtility(), FileUtility())
            location_list = self.location_list(chunk_list, zip.file_utility.rootDir('media/export'))
            zip_it.download(project_to_find, location_list)
        return Response(status=200)

    def chunk_list(self, data):
        project_to_find = {}
        if 'language' in data and 'version' in data and 'book' in data:
            project_to_find['language'] = data['language']
            project_to_find['version'] = data['version']
            project_to_find['book'] = data['book']
        return project_to_find, Chunk.getChunksWithTakesByProject(project_to_find)

    def location_list(self, project, root_directory):
        chapter_directory = ""
        locations = []
        for chunk in project["chunks"]:
            for take in chunk['takes']:
                chapter_directory = root_directory
                + os.sep + project['language']["slug"]
                + os.sep + project['project']['version']
                + os.sep + project['book']['slug'] + os.sep
                + str(project['chapter']['number'])

                if not os.path.exists(chapter_directory):
                    os.makedirs(chapter_directory)
                location = {}
                location["src"] = os.path.join(
                    settings.BASE_DIR, take["take"]["locationation"])
                location["dst"] = chapter_directory
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
