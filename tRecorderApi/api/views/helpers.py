import hashlib
import os
import re

from pydub import AudioSegment


def md5Hash(filename):
    hash_md5 = hashlib.md5()
    try:
        with open(filename, "rb") as file:
            for chunk in iter(lambda: file.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except:
        return ""


def getFileName(location):
    return location.split(os.sep)[-1]


def getFilePath(location):
    list = location.split(os.sep)[3:]
    return "/".join(list)


def highPassFilter(location):
    song = AudioSegment.from_wav(location)
    new = song.high_pass_filter(80)
    new.export(location, format="wav")


def getRelativePath(location):
    reg = re.search('(media\/.*)$', location)
    return reg.group(1)
