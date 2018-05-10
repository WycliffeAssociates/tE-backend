import datetime

from .FileTransfer import FileTransfer
from api.tasks import download_project


class Download(FileTransfer):
    def __init__(self, archive_project, audio_utility, file_utility):
        super().__init__(archive_project, audio_utility, file_utility)

    def download(self, project, location_list, root_dir, file_format, user):
        title = "Download project"
        started = datetime.datetime.now()
        task = download_project.delay(self, project, root_dir, location_list, file_format,
                                      title=title,
                                      started=started,
                                      user_icon_hash=user.icon_hash)

        return task.id

