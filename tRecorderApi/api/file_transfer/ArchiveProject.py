from abc import ABCMeta, abstractmethod


#interface
class ArchiveProject(metaclass=ABCMeta):

    @abstractmethod
    def archive(directory):
       pass

    @abstractmethod
    def extract(file, directory):
        pass
