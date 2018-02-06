from .FileTransfer import FileTransfer


class Upload(FileTransfer):

    def __init__(self, archive_project, audio_utility, file_utility
                 ):  # these objects come from file transfer

        super().__init__(archive_project, audio_utility, file_utility)

    def upload(self, file):
        directory = self.file_utility.root_dir(['media', 'dump'])
        resp, stat = self.archive_project.extract(file, directory)   #returns response, status
        if resp == 'ok':
            resp, stat = self.file_utility.import_project(directory)
        return resp, stat
