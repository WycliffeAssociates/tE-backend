import zipfile
from io import BytesIO

from .ArchiveProject import ArchiveProject


class ArchiveIt(ArchiveProject):
    def archive(self, root_dir, project_file, files_in_zip, remove_dir):
        with zipfile.ZipFile(project_file, 'w') as zipped_f:
            for file in files_in_zip:
                zipped_f.write(file, file.replace(root_dir, ""))

        remove_dir(root_dir)
        return project_file

    def archive_in_memory(self, files_list):
        in_memory_zip = BytesIO()

        with zipfile.ZipFile(in_memory_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
            for file_obj in files_list:
                zf.writestr(file_obj["file_path"], file_obj["file_contents"])

        return in_memory_zip.getvalue()

    def extract(self):
        pass
