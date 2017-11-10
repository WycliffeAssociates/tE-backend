import shutil

import os
import time
import uuid


class FileUtility:
    def rootDir(self, root_dir_of):
        uuid_name = str(time.time()) + str(uuid.uuid4())
        root_directory = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))).BASE_DIR, root_dir_of, uuid_name)
        if not os.path.exists(root_directory):
            return os.makedirs(root_directory)
        return root_directory

    def copy_files_from_src_to_dest(self, location_list):
        for location in location_list:
            shutil.copy2(location["src"], location["dst"])

    def project_file(self, project_name, dir_of, file_extension):
        return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))).BASE_DIR, dir_of,
                            file_extension)
