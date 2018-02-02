from .FileTransfer import FileTransfer


class Upload(FileTransfer):

    def __init__(self, archive_project, audio_utility, file_utility,
                 take_database):  # these objects come from file transfer
        self.take_database = take_database
        super().__init__(archive_project, audio_utility, file_utility)

    def upload(self, file, ext):
        directory = self.file_utility.root_dir(['media','dump'])
        resp, stat = self.archive_project.extract(file, directory)   #returns response, status
        if resp == 'ok':
            resp, stat = self.file_utility.import_project(directory, self.take_database, ext)
        return resp, stat
