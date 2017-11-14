from .ArchiveProject import ArchiveProject


class TrIt(ArchiveProject):

    def archive(self):
        print("zipped")

    def extract(self):
        pass
