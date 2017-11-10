import os
import shutil
import zipfile

from rest_framework.response import Response

from .helpers import (zip_files_root_directory, remove_file_tree)


def zip_it(data):
    if 'language' in data and 'version' in data and 'book' in data:
        project = Chunk.getChunksWithTakesByProject(data)

        if(len(project['chunks']) > 0):

            project_root_directory = zip_files_root_directory()

            project_zip_file_destination = self.project_zip_file_path(
                project)

            locations = self.take_location_list(
                project, project_root_directory)

            self.copy_files_from_src_to_dest(locations)
            self.zip_project(
                project_root_directory, project_zip_file_destination)
        else:
            return Response({"error": "no_files"}, status=400)
    else:
        return Response({"error", "not_enough_parameters"}, status=400)

    def project_zip_file_path(self, project):

        project_name = project['language']["slug"]
        + "_" + project['project']['version']
        +"_" + project['book']['slug']
        return path('media/export', project_name, '.zip')

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

    def copy_files_from_src_to_dest(self, location_list):
        for location in location_list:
            shutil.copy2(location["src"], location["dst"])

    def zip_project(self, project_root_directory, project_file):

        # list of mp3 files
        filesInZip = convert_wav_mp3(project_root_directory)

        # Creating zip file
        with zipfile.ZipFile(project_file, 'w') as zipped_f:
            for members in filesInZip:
                zipped_f.write(
                    members, members.replace(project_root_directory, ""))
        # remove wav files directory
        remove_file_tree(project_root_directory)

        return Response(
            {
                "location": getRelativePath(project_file)
            },
            status=200)

    def convert_wav_mp3(project_root_directory):
        filesInZip = []
        for subdir in os.walk(project_root_directory):
            for file in files:
                filePath = subdir + os.sep + file
                if filePath.endswith(".wav"):
                    # Add to array so it can be added to the archive
                    sound = AudioSegment.from_wav(filePath)
                    filename = filePath.replace(".wav", ".mp3")
                    sound.export(filename, format="mp3")
                    filesInZip.append(filename)
                else:
                    filesInZip.append(filePath)
        return filesInZip
