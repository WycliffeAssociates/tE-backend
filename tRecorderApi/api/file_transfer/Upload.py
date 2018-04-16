from .FileTransfer import FileTransfer
from ..tasks import extract_and_save_project, cleanup_orphan_files


class Upload(FileTransfer):

    # these objects come from file transfer
    def __init__(self, archive_project, audio_utility, file_utility):
        super().__init__(archive_project, audio_utility, file_utility)

    def upload(self, file):
        directory = self.file_utility.root_dir(['media', 'dump'])
        chain = extract_and_save_project.s(self, file, directory) | \
            cleanup_orphan_files.s(self)

        chain()
