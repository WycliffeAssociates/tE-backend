from .FileTransfer import FileTransfer


class Upload(FileTransfer):

    def __init__(self, archive_project, audio_utility, file_utility,
                 take_database):  # these objects come from file transfer
        self.takeDatabase = take_database
        super().__init__(archive_project, audio_utility, file_utility)

    def upload(self, file, ext):
        directory = self.file_utility.root_dir(['media', 'dump'])
        resp, stat = self.archive_project.extract(file, directory)
        if resp == 'ok':
            return self.file_utility.process_uploaded_takes(directory, self.takeDatabase, ext)
        else:
            return {"status": 'processing'}
