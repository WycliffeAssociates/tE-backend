from .ArchiveProject import ArchiveProject
from .FileUtility import FileUtility


class TrIt(ArchiveProject):

    def archive(self):
        print("zipped")

    def extract(self, file, directory):
        fl = FileUtility()
        resp, stat = fl.processTrFile(file, directory)
        return resp, stat

