import zipfile

from .ArchiveProject import ArchiveProject


class ZipIt(ArchiveProject):
    def archive(self, root_dir, project_file, files_in_zip):
        filelocation = None
        with zipfile.ZipFile(project_file, 'w') as zipped_f:
            for file in files_in_zip:
                zipped_f.write(file, file.replace(root_dir, ""))
                filelocation = file
        return filelocation

    def extract(self):
        pass
