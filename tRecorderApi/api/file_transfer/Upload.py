from .FileTransfer import FileTransfer
from ..tasks import extract_process_file


class Upload(FileTransfer):

    def __init__(self, archive_project, audio_utility, file_utility,
                 take_database):  # these objects come from file transfer
        self.takeDatabase = take_database
        super().__init__(archive_project, audio_utility, file_utility)

    def upload(self, file, ext):
        directory = self.file_utility.root_dir(['media', 'dump'])
        result = extract_process_file.delay(self, directory, file, self.takeDatabase, ext)
        if result.ready:
            return result.get()
        else:
            return {"status": 'processing'}
