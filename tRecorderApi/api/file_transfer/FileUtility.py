import os
import shutil
import time
import uuid


class FileUtility:
    def rootDir(self, rootDirOf):
        directory = ''
        for dir in rootDirOf:
            directory += dir + "/"
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        uuid_name = str(time.time()) + str(uuid.uuid4())
        root_directory = os.path.join(base_dir, directory + uuid_name)
        if not os.path.exists(root_directory):
            os.makedirs(root_directory)
        return root_directory

    def createPath(self, root_dir, lang_slug, version, book_slug, chapter_number):
        path = os.path.join(root_dir, lang_slug, version, book_slug, chapter_number)

        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def take_location(self, take_location):
        return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                            take_location)

    def copy_files_from_src_to_dest(self, location_list):

        for location in location_list:
            shutil.copy2(location["src"], location["dst"])

    def project_file(self, project_name, dir_of, file_extension):

        return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), dir_of,
                            project_name + file_extension)

    def remove_dir(self, dir_to_remove):

        shutil.rmtree(dir_to_remove)
