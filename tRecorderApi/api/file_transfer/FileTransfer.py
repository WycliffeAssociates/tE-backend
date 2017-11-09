from ArchiveProject import ArchiveProject
from AudioUtility import AudioUtility
from FileUtility import FileUtility
from abc import ABCMeta


class FileTransfer(metaclass=ABCMeta):

    def __init__(self, archive_project, audio_utility, file_utility):
        self.archive_project = ArchiveProject
        self.audio_utility = AudioUtility
        self.file_utility = FileUtility
