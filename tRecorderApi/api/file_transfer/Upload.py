from .FileTransfer import FileTransfer
from ..tasks import get_project


class Upload(FileTransfer):

    def __init__(self, archive_project, audio_utility, file_utility
                 ):  # these objects come from file transfer

        super().__init__(archive_project, audio_utility, file_utility)

    def upload(self, file):
        directory = self.file_utility.root_dir(['media', 'dump'])
        result = get_project.delay(self, file, directory)
        if result.ready:
            return result.get()
