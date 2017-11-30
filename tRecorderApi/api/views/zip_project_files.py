import os
import shutil
import time
import uuid
import zipfile
from api.models import Chunk
from django.conf import settings
from .helpers import get_relative_path
from pydub import AudioSegment
from rest_framework import views
from rest_framework.parsers import JSONParser
from rest_framework.response import Response


class ZipProjectFiles(views.APIView):
    parser_classes = (JSONParser,)

    def post(self, request):
        data = request.data
        project_to_find = {}
        if 'language' in data and 'version' in data and 'book' in data:
            uuid_name = str(time.time()) + str(uuid.uuid4())
            project_root_directory = os.path.join(
                settings.BASE_DIR, 'media/export', uuid_name)
            if not os.path.exists(project_root_directory):
                os.makedirs(project_root_directory)

            project_to_find['language__slug'] = data['language']['slug']
            project_to_find['version__slug'] = data['version']['slug']
            project_to_find['book__slug'] = data['book']['slug']
            project_to_find['book__number'] = data['book']['number']

            project = Chunk.getChunksWithTakesByProject(project_to_find)

            if(len(project['chunks']) > 0):
                project_zip_file = self.project_zip_file_destination(
                    project)
                locations = self.take_location_list
                self.copy_files_from_src_to_dest(locations)
                self.zip_project(project_root_directory, project_zip_file)
            else:
                return Response({"error": "no_files"}, status=400)
        else:
            return Response({"error", "not_enough_parameters"}, status=400)

        def project_zip_file(self, project, root_project_directory):
            uuid_name = str(time.time()) + str(uuid.uuid4())
            root_project_directory = os.path.join(
                settings.BASE_DIR, 'media/export', uuid_name)
            project_name = project['language']["slug"]
            + "_" + project['project']['version']
            +"_" + project['book']['slug']
            return os.path.join(settings.BASE_DIR,
                                'media/export',
                                project_name + ".zip")

        def take_location_list(self, project, project_root_directory):
            chapter_directory = ""
            locations = []
            for chunk in project["chunks"]:
                for take in chunk['takes']:
                    chapter_directory = project_root_directory
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

        def copy_files_from_src_to_dest(self, lication_list):
            # TODO:discuss if this function needs to go in background process
            for location in lication_list:
                shutil.copy2(location["src"], location["dst"])

        def zip_project(self, project_root_directory, project_file):
            filesInZip = []
            for subdir in os.walk(project_root_directory):
                for file in files:
                    # store the absolute path which is it's subdir and where
                    # the os step is
                    filePath = subdir + os.sep + file
                    if filePath.endswith(".wav"):
                        # Add to array so it can be added to the archive
                        sound = AudioSegment.from_wav(filePath)
                        filename = filePath.replace(".wav", ".mp3")
                        sound.export(filename, format="mp3")
                        filesInZip.append(filename)
                    else:
                        filesInZip.append(filePath)

            # Creating zip file
            with zipfile.ZipFile(project_file, 'w') as zipped_f:
                for members in filesInZip:
                    zipped_f.write(
                        members, members.replace(project_root_directory, ""))

            shutil.rmtree(project_root_directory)
            return Response(
                {
                    "location": get_relative_path(project_file)
                },
                status=200)

    # def post1(self, request):
    #     data = request.data
    # TODO:Discuss what this check is doing
    #     if "project" not in data:
    #         if 'language' not in data or 'version' not in data \
    #                 or "book" not in data:
    # return Response({"error", "not_enough_parameters"}, status=400)

    #     new_data = {}
    #     if "project" in data:
    #         new_data["project"] = data["project"]
    #     else:
    #         new_data["language"] = data["language"]
    #         new_data["version"] = data["version"]
    #         new_data["book"] = data["book"]
    # new_data["is_publish"] = True

    #     project = Chunk.getChunksWithTakesByProject(new_data)

    #     if len(project["chunks"]) > 0:
    #         uuid_name = str(time.time()) + str(uuid.uuid4())
    #         root_folder = os.path.join(
    #             settings.BASE_DIR, 'media/export', uuid_name)

    #         project_name = project['language']["slug"] + \
    #             "_" + project['project']['version'] + \
    #             "_" + project['book']['slug']
    #         project_file = os.path.join(
    #             settings.BASE_DIR, 'media/export', project_name + ".zip")

    #         if not os.path.exists(root_folder):
    #             os.makedirs(root_folder)

    # create list for locations
    #         chapter_folder = ""
    #         locations = []
    #         for chunk in project["chunks"]:
    #             for take in chunk['takes']:
    #                 chapter_folder = root_folder + os.sep + project['language']["slug"] + \
    #                     os.sep + project['project']['version'] + \
    #                     os.sep + project['book']['slug'] + \
    #                     os.sep + str(project['chapter']['number'])

    #                 if not os.path.exists(chapter_folder):
    #                     os.makedirs(chapter_folder)

    #                 location = {}
    #                 location["src"] = os.path.join(
    #                     settings.BASE_DIR, take["take"]["locationation"])
    #    																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																								             location["dst"] = chapter_folder
    #                 locations.append(location)

    # use shutil to copy the wav files to a new folder
    #         for location in locationations:
    #             shutil.copy2(location["src"], location["dst"])

    # process of renaming/converting to mp3

    #         filesInZip = []

    #         for subdir, dirs, files in os.walk(root_folder):
    #             for file in files:
    # store the absolute path which is is it's subdir and where
    # the os step is
    #                 filePath = subdir + os.sep + file
    #                 if filePath.endswith(".wav"):
    # Add to array so it can be added to the archive
    #                     sound = AudioSegment.from_wav(filePath)
    #                     filename = filePath.replace(".wav", ".mp3")
    #                     sound.export(filename, format="mp3")
    #                     filesInZip.append(filename)
    #                 else:
    #                     filesInZip.append(filePath)

    # Creating zip file
    #         with zipfile.ZipFile(project_file, 'w') as zipped_f:
    #             for members in filesInZip:
    #                 zipped_f.write(members, members.replace(root_folder, ""))

    # delete the newly created wave and mp3 files
    #         shutil.rmtree(root_folder)
    #         return Response({"location": getRelativePath(project_file)}, status=200)
    #     else:
    #         return Response({"error": "no_files"}, status=400)

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