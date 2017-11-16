from pydub import AudioSegment
from tinytag import TinyTag
import subprocess
import os
import time
import re
import uuid
import json
import urllib.error, urllib.request
import pickle
import urllib3
import shutil


class FileUtility:
    def convertTomp3(self, directory):
        return print('mp3 converted', directory)

    def highPassFilter(self, directory):
        song = AudioSegment.from_wav(directory)
        new = song.high_pass_filter(80)
        new.export(self.filePath, format="wav")

    def rootDir(self, rootDirOf):
        directory = ''
        for dir in rootDirOf:
            directory += dir + '/'
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        uuid_name = str(time.time()) + str(uuid.uuid4())
        root_directory = os.path.join(
            base_dir, directory + uuid_name)
        if not os.path.exists(root_directory):
            os.makedirs(root_directory)
        return root_directory

    def copy_files_from_src_to_dest(self, location_list):
        for location in location_list:
            shutil.copy2(location["src"], location["dst"])

    def processUploadedTakes(self, directory, Take, ext):
        if ext == 'tr':
            os.remove(os.path.join(directory, "source.tr"))

        for root, dirs, files in os.walk(directory):
            for f in files:
                abpath = os.path.join(root, os.path.basename(f))
                relpath = self.getRelativePath(abpath)
                try:
                    meta = TinyTag.get(abpath)  # get metadata for every file
                except LookupError as e:
                    return {'error': 'bad_wave_file'}, 400

                data, pls = self.createObjectFromMeta(meta)
                # highPassFilter(abpath)
                is_source_file = False
                if ext == "tr":
                    is_source_file = True

                Take.saveTakesToDB(pls, relpath, data, is_source_file)

        return 'ok', 200

    def createObjectFromMeta(self, meta):
        try:
            a = meta.artist
            lastindex = a.rfind("}") + 1
            substr = a[:lastindex]
            pls = json.loads(substr)

            bookcode = pls['slug']
            bookname = self.getBookByCode(bookcode)
            langcode = pls['language']
            langname = self.getLanguageByCode(langcode)

            data = {
                "langname": langname,
                "bookname": bookname,
                "duration": meta.duration
            }
            return data, pls
        except Exception as e:
            return "bad zip file", 400

    @staticmethod
    def getRelativePath(location):
        reg = re.search('(media\/.*)$', location)
        return reg.group(1)

    @staticmethod
    def getLanguageByCode(code):
        url = 'http://td.unfoldingword.org/exports/langnames.json'
        http = urllib3.PoolManager()
        request = http.request('GET', url)
        languages = []
        try:
            languages = json.loads(request.data.decode('utf8'))
            with open('language.json', 'wb') as fp:
                pickle.dump(languages, fp)
        except urllib.error.URLError as e:
            with open('language.json', 'rb') as fp:
                languages = pickle.load(fp)

        ln = ""
        for dicti in languages:
            if dicti["lc"] == code:
                ln = dicti["ln"]
                break
        return ln

    @staticmethod
    def getBookByCode(code):
        with open('books.json') as books_file:
            books = json.load(books_file)

        bn = ""
        for dicti in books:
            if dicti["slug"] == code:
                bn = dicti["name"]
                break
        return bn

    @staticmethod
    def processTrFile(file, directory):
        with open(os.path.join(directory, "source.tr"), 'wb') as temp_file:
            for line in file:
                temp_file.write(line)
            try:
                FNULL = open(os.devnull, 'wb')
                base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

                path = os.path.join(base_dir, 'aoh/aoh.jar')
                file_path = os.path.join(os.path.join(directory, "source.tr"))

                subprocess.check_output(
                    ['java', '-jar', os.path.join(base_dir, 'aoh/aoh.jar'), '-x', file_path],
                    stderr=subprocess.STDOUT
                )
                FNULL.close()
                #os.remove(os.path.join(directory, "source.tr"))

                return 'ok', 200

            except Exception as e:
            #shutil.rmtree(directory)
                return str(e), 400
