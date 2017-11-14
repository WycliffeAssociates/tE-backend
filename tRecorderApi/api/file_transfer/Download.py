from FileTransfer import FileTransfer


class Download(FileTransfer):

    def __init__(self, archive_project, audio_utility, file_utility):
        super().__init__(archive_project, audio_utility, file_utility)

    def download(self):
        self.audio_utility.convert_to_mp3()
        self.file_utility.file_path_list()
        self.archive_project.archive("directory")
