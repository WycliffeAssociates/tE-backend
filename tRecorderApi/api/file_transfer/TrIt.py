from .ArchiveProject import ArchiveProject
from .FileUtility import FileUtility


class TrIt(ArchiveProject):

    def archive(self):
        print("zipped")

    def extract(self, file, directory, temp):
        fl = FileUtility()
        resp, stat = fl.processTrFile(file, directory, temp)
        return resp, stat

