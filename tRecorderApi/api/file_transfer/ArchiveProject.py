from abc import ABCMeta, abstractmethod


class ArchiveProject(metaclass=ABCMeta):

    @abstractmethod
    def archive(rootDir,project_file, converted_mp3):
        pass

    @abstractmethod
    def extract():
        pass
