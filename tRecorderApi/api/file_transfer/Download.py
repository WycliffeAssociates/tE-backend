from .FileTransfer import FileTransfer


class Download(FileTransfer):
    def __init__(self, archive_project, audio_utility, file_utility):
        super().__init__(archive_project, audio_utility, file_utility)

    def download(self, project_name, location_list):
        root_dir = self.file_utility.rootDir('media/export')
        project_file = self.file_utility(project_name, 'media/export', '.zip')
        self.file_utility.copy_files_from_src_to_dest(
            self, location_list)
        self.audio_utility.convert_to_mp3(root_dir)
        self.archive_project.archive(root_dir, project_file,location_list)
