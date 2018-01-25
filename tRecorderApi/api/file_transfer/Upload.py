from .FileTransfer import FileTransfer
from ..tasks import extract


class Upload(FileTransfer):

    def __init__(self, archive_project, audio_utility, file_utility,
                 take_database):  # these objects come from file transfer
        self.takeDatabase = take_database
        super().__init__(archive_project, audio_utility, file_utility)

    def upload(self, file, ext):
        directory = self.file_utility.root_dir(['media', 'dump'])
        result = extract.delay(file, directory)
        if result.ready:
            resp, stat = self.file_utility.process_uploaded_takes(directory, self.takeDatabase, ext)
            return resp, stat
        else:
            return {"status": 'processing'}
