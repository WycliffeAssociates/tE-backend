# from os import remove

import glob
import hashlib
import json
import os
import pickle
import shutil
import subprocess
import time
import urllib2
import uuid
import zipfile
from random import randint
import pydub
from django.conf import settings
from django.core import files
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from pydub import AudioSegment
from rest_framework import viewsets, views, status
from rest_framework.generics import ListAPIView
from rest_framework.parsers import JSONParser, FileUploadParser, MultiPartParser, FormParser
from rest_framework.parsers import JSONParser, FileUploadParser
from rest_framework.response import Response
from tinytag import TinyTag
from .models import Language, Book, User, Take, Comment
from .serializers import LanguageSerializer, BookSerializer, UserSerializer
from .serializers import TakeSerializer, CommentSerializer


class LanguageViewSet(viewsets.ModelViewSet):
    """This class handles the http GET, PUT, PATCH, POST and DELETE requests."""
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class BookViewSet(viewsets.ModelViewSet):
    """This class handles the http GET, PUT, PATCH, POST and DELETE requests."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class UserViewSet(viewsets.ModelViewSet):
    """This class handles the http GET, PUT, PATCH, POST and DELETE requests."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TakeViewSet(viewsets.ModelViewSet):
    """This class handles the http GET, PUT, PATCH, POST and DELETE requests."""
    queryset = Take.objects.all()
    serializer_class = TakeSerializer

    def destroy(self, request, pk=None):
        instance = self.get_object()
        try:
            os.remove(instance.location)
        except OSError:
            pass
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    """This class handles the http GET, PUT, PATCH, POST and DELETE requests."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def destroy(self, request, pk=None):
        instance = self.get_object()
        try:
            os.remove(instance.location)
        except OSError:
            pass
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)


class ProjectView(views.APIView):
    """This class handles the http POST requests."""
    parser_classes = (JSONParser,)

    def post(self, request):
        data = json.loads(request.body)
        lst = getTakesByProject(data)

        return Response(lst, status=200)


class ProjectZipFiles(views.APIView):
    parser_classes = (JSONParser,)

    def post(self, request):
        data = request.data
        new_data = {}
        wavfiles = []

        # filter the database with the given parameters
        if "language" in data:
            new_data["language"] = data["language"]
        if "version" in data:
            new_data["version"] = data["version"]
        if "book" in data:
            new_data["book"] = data["book"]

        if 'language' in new_data and 'version' in new_data and 'book' in new_data:
            lst = getTakesByProject(new_data)

            filesInZip = []
            uuid_name = str(time.time()) + str(uuid.uuid4())
            root_folder = 'media/export/' + uuid_name
            chapter_folder = ""
            project_name = new_data["language"] + \
                "_" + new_data["version"] + \
                "_" + new_data["book"]

            # create list for locations
            locations = []
            for i in lst:
                chapter_folder = root_folder + os.sep + i["language"]["slug"] + \
                    os.sep + i["take"]["version"] + \
                    os.sep + i["book"]["slug"] + \
                    os.sep + str(i["take"]["chapter"])
                
                if not os.path.exists(chapter_folder):
                    os.makedirs(chapter_folder)

                loc = {}
                loc["src"] = i["take"]["location"]
                loc["dst"] = chapter_folder
                locations.append(loc)

            # use shutil to copy the wav files to a new file
            for loc in locations:
                shutil.copy2(loc["src"], loc["dst"])

            # process of renaming/converting to mp3
            for subdir, dirs, files in os.walk(root_folder):
                for file in files:
                    # store the absolute path which is is it's subdir and where the os step is
                    filePath = subdir + os.sep + file

                    if filePath.endswith(".wav") or filePath.endswith(".mp3"):
                        # Add to array so it can be added to the archive
                        sound = AudioSegment.from_wav(filePath)
                        filename = filePath.replace(".wav", ".mp3")
                        sound.export(filename, format="mp3")
                        filesInZip.append(filename)

            # Creating zip file
            with zipfile.ZipFile('media/export/' + project_name + '.zip', 'w') as zipped_f:
                for members in filesInZip:
                    zipped_f.write(members, members.replace(root_folder,""))

            # delete the newly created wave and mp3 files
            shutil.rmtree(root_folder)

            return Response(lst, status=200)
        else:
            return Response({"response":"notenoughparameters"}, status=403)

class FileUploadView(views.APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request, filename, format='zip'):
        if request.method == 'POST' and request.data['file']:
            uuid_name = str(time.time()) + str(uuid.uuid4())
            upload = request.data["file"]

            # unzip files
            try:
                zip = zipfile.ZipFile(upload)
                folder_name = 'media/dump/' + uuid_name

                zip.extractall(folder_name)
                zip.close()

                # extract metadata / get the apsolute path to the file to be stored

                # Cache language and book to re-use later
                bookname = ''
                bookcode = ''
                langname = ''
                langcode = ''

                for root, dirs, files in os.walk(folder_name):
                    for f in files:
                        abpath = os.path.join(root, os.path.basename(f))
                        # abpath = os.path.abspath(os.path.join(root, f))
                        try:
                            meta = TinyTag.get(abpath)
                        except LookupError:
                            return Response({"response": "badwavefile"}, status=403)
                        
                        if meta and meta.artist:
                            a = meta.artist
                            lastindex = a.rfind("}") + 1
                            substr = a[:lastindex]
                            pls = json.loads(substr)

                            if bookcode != pls['slug']:
                                bookcode = pls['slug']
                                bookname = getBookByCode(bookcode)
                            if langcode != pls['language']:
                                langcode = pls['language']
                                langname = getLanguageByCode(langcode)

                            data = {
                                "langname": langname,
                                "bookname": bookname,
                                "duration": meta.duration
                                }
                            prepareDataToSave(pls, abpath, data)
                        else:
                            return Response({"response": "badwavefile"}, status=403)
                return Response({"response": "ok"}, status=200)

            except zipfile.BadZipfile:
                return Response({"response": "badzipfile"}, status=403)
        else:
            return Response(status=404)


class FileStreamView(views.APIView):
    def get(self, request, filepath, format='mp3'):
        sound = pydub.AudioSegment.from_wav(filepath)
        file = sound.export()
        return StreamingHttpResponse(file)


class SourceFileView(views.APIView):
    parser_classes = (JSONParser,)

    def post(self, request):
        #if not os.path.exists('media/tmp/'+lang+'_'+ver+'.tr'):
        data = request.data
        data["is_source"] = True
        takes = getTakesByProject(data)

        if 'language' in data and 'version' in data:
            if len(takes) > 0:
                uuid_name = str(time.time()) + str(uuid.uuid4())
                root_folder = 'media/tmp/' + uuid_name
                project_folder = root_folder + '/' + data['language'] + '/' + data['version']
                for take in takes:
                    chapter_folder = project_folder + '/' + take['book']['slug'] + '/' + str(
                        take['take']['chapter']).zfill(2)
                    if not os.path.exists(chapter_folder):
                        os.makedirs(chapter_folder)
                    shutil.copy2(take['take']['location'], chapter_folder)
                    file_name = os.path.basename(take['take']['location'])
                    file_path = chapter_folder + '/' + file_name
                    file_path_mp3 = file_path.replace('.wav', '.mp3')

                    sound = pydub.AudioSegment.from_wav(file_path)
                    sound.export(file_path_mp3, format='mp3')
                    os.remove(file_path)

                FNULL = open(os.devnull, 'w')
                subprocess.call(['java', '-jar', 'aoh/aoh.jar', '-c', '-tr', root_folder],
                                stdout=FNULL, stderr=subprocess.STDOUT)
                FNULL.close()
                os.rename(root_folder+'.tr', 'media/tmp/'+data['language']+'_'+data['version']+'.tr')
                shutil.rmtree(root_folder)
            else:
                return Response({"response": "nosource"}, status=403)
        else:
            return Response({"response": "notenoughparameters"}, status=403)

        source_file = open('media/tmp/' + data['language'] + '_' + data['version'] + '.tr', 'rb')
        response = HttpResponse(files.File(source_file), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="%s"' % (
            data['language'] + '_' + data['version'] + '.tr')
        source_file.close()
        return response


class ExcludeFilesView(views.APIView):
    parser_classes = (JSONParser,)

    def post(self, request):
        files_to_exclude = {}
        data = json.loads(request.body)
        takes = getTakesByProject(data)
        for take in takes:
            location = take['take']['location']
            files_to_exclude[getFileName(location)] = md5Hash(location)
        return Response(files_to_exclude, status=200)


def index(request):
    take = Take.objects.all().last()
    return render(request, 'index.html', {"lasttake": take})


def getTakesByProject(data):
    lst = []
    takes = Take.objects
    if "language" in data:
        takes = takes.filter(language__slug=data["language"])
    if "version" in data:
        takes = takes.filter(version=data["version"])
    if "book" in data:
        takes = takes.filter(book__slug=data["book"])
    if "chapter" in data:
        takes = takes.filter(chapter=data["chapter"])
    if "startv" in data:
        takes = takes.filter(startv=data["startv"])
    if "is_source" in data: 
        takes = takes.filter(is_source=data["is_source"])
    
    res = takes.values()

    for take in res:
        dic = {}
        # Include language name
        lang = Language.objects.filter(pk=take["language_id"])
        if lang and lang.count() > 0:
            dic["language"] = lang.values()[0]
        # Include book name
        book = Book.objects.filter(pk=take["book_id"])
        if book and book.count() > 0:
            dic["book"] = book.values()[0]
        # Include author of file
        user = User.objects.filter(pk=take["user_id"])
        if user and user.count() > 0:
            dic["user"] = user.values()[0]

        # Include comments
        dic["comments"] = []
        for cmt in Comment.objects.filter(file=take["id"]).values():
            dic2 = {}
            dic2["comment"] = cmt
            # Include author of comment
            cuser = User.objects.filter(pk=cmt["user_id"])
            if cuser and cuser.count() > 0:
                dic2["user"] = cuser.values()[0]
            dic["comments"].append(dic2)

        # Parse markers
        if take["markers"]:
            take["markers"] = json.loads(take["markers"])
        else:
            take["markers"] = {}
        dic["take"] = take
        lst.append(dic)
    return lst


def prepareDataToSave(meta, abpath, data):
    book, b_created = Book.objects.get_or_create(
        slug=meta["slug"],
        defaults={'slug': meta['slug'], 'booknum': meta['book_number'], 'name': data['bookname']},
    )
    language, l_created = Language.objects.get_or_create(
        slug=meta["language"],
        defaults={'slug': meta['language'], 'name': data['langname']},
    )
    markers = json.dumps(meta['markers'])
    take = Take(location=abpath,
                duration = data['duration'],
                book = book,
                language = language,
                rating = 0, checked_level = 0,
                anthology = meta['anthology'],
                version = meta['version'],
                mode = meta['mode'],
                chapter = meta['chapter'],
                startv = meta['startv'],
                endv = meta['endv'],
                markers = markers,
                is_export=True,
                is_source=False,
                user_id = 1) # TODO get author of file and save it to Take model
    take.save()


def getLanguageByCode(code):
    url = 'http://td.unfoldingword.org/exports/langnames.json'
    languages = []
    try:
        response = urllib2.urlopen(url)
        languages = json.loads(response.read())
        with open('language.json', 'wb') as fp:
            pickle.dump(languages, fp)
    except urllib2.URLError, e:
        with open('language.json', 'rb') as fp:
            languages = pickle.load(fp)

    ln = ""
    for dicti in languages:
        if dicti["lc"] == code:
            ln = dicti["ln"]
            break
    return ln


def getBookByCode(code):
    with open('books.json') as books_file:
        books = json.load(books_file)

    bn = ""
    for dicti in books:
        if dicti["slug"] == code:
            bn = dicti["name"]
            break
    return bn


def md5Hash(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def getFileName(location):
    return location.split(os.sep)[-1]
