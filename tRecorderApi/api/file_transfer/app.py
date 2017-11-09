
from Download import Download
from ZipIt import ZipIt
from TrIt import TrIt
from AudioUtility import AudioUtility
from FileUtility import FileUtility
import time

# downloading zip
zip = Download(ZipIt(), AudioUtility(), FileUtility())
print("Downloading....")
time.sleep(5)
zip.download()
print("zip completed.")

# sending tr to TRecorder
tr = Download(TrIt(), AudioUtility(), None)
print("Downloading tr...")
time.sleep(5)
tr.download()
print("tr downloaded.")
