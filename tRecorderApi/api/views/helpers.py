import json
import pickle
import urllib2
import os
import hashlib
import zipfile
from pydub import AudioSegment, effects
from django.db.models import Prefetch
import re

def md5Hash(fname):
    hash_md5 = hashlib.md5()
    try:
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
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
    new.export(location, format = "wav")

def getRelativePath(location):
        reg = re.search('(media\/.*)$', location)
        return reg.group(1)