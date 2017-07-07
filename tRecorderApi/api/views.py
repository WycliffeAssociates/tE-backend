from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.core import serializers, files
from rest_framework import viewsets, views, status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FileUploadParser
from api.parsers import MP3StreamParser
from .serializers import LanguageSerializer, BookSerializer, UserSerializer
from .serializers import TakeSerializer, CommentSerializer
from .models import Language, Book, User, Take, Comment
from tinytag import TinyTag
import zipfile
import urllib2
import pickle
import json
import pydub
import time
import uuid
import os
import subprocess
import shutil

class LanguageViewSet(viewsets.ModelViewSet):
    """This class handles the http GET, PUT and DELETE requests."""
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

class BookViewSet(viewsets.ModelViewSet):
    """This class handles the http GET, PUT and DELETE requests."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class UserViewSet(viewsets.ModelViewSet):
    """This class handles the http GET, PUT and DELETE requests."""
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TakeViewSet(viewsets.ModelViewSet):
    """This class handles the http GET, PUT and DELETE requests."""
    queryset = Take.objects.all()
    serializer_class = TakeSerializer

    def destroy(self, request, pk = None):
        instance = self.get_object()
        try:
            os.remove(instance.location)
        except OSError:
            pass
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)

class CommentViewSet(viewsets.ModelViewSet):
    """This class handles the http GET, PUT and DELETE requests."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def destroy(self, request, pk = None):
        instance = self.get_object()
        try:
            os.remove(instance.location)
        except OSError:
            pass
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)

class ProjectViewSet(views.APIView):
    parser_classes = (JSONParser,)

    def post(self, request):
        data = json.loads(request.body)
        lst = getTakesByProject(data)
        return Response(lst, status=200)

class FileUploadView(views.APIView):
    parser_classes = (FileUploadParser,)
    def post(self, request, filename, format='zip'):
        if request.method == 'POST' and request.data['file']:
            uuid_name = str(time.time()) + str(uuid.uuid4())
            upload = request.data["file"]
            #unzip files
            try:
                zip = zipfile.ZipFile(upload)
                file_name = 'media/dump/' + uuid_name
                zip.extractall(file_name)
                zip.close()
                #extract metadata / get the apsolute path to the file to be stored

                # Cache language and book to re-use later
                bookname = ''
                bookcode = ''
                langname = ''
                langcode = ''

                for root, dirs, files in os.walk(file_name):
                    for f in files:
                        abpath = os.path.join(root, os.path.basename(f))
                        try:
                            meta = TinyTag.get(abpath)
                        except LookupError:
                            return Response({"response": "badwavefile"}, status=403)

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
    def get(self, request, lang, ver):
        if not os.path.exists('media/tmp/'+lang+'_'+ver+'.tr'):
            takes = getTakesByProject({"language":lang,"version":ver})
            
            if len(takes) > 0:
                uuid_name = str(time.time()) + str(uuid.uuid4())
                root_folder = 'media/tmp/'+uuid_name
                project_folder = root_folder+'/'+lang+'/'+ver
                for take in takes:
                    chapter_folder = project_folder+'/'+take['book']['slug']+'/'+str(take['take']['chapter']).zfill(2)
                    if not os.path.exists(chapter_folder):
                        os.makedirs(chapter_folder)
                    shutil.copy2(take['take']['location'], chapter_folder)
                    file_name = os.path.basename(take['take']['location'])
                    file_path = chapter_folder+'/'+file_name
                    file_path_mp3 = file_path.replace('.wav','.mp3')

                    sound = pydub.AudioSegment.from_wav(file_path)
                    sound.export(file_path_mp3, format='mp3')
                    os.remove(file_path)
                
                FNULL = open(os.devnull, 'w')
                subprocess.call(['java', '-jar', 'aoh/aoh.jar', '-c', '-tr', root_folder], 
                    stdout=FNULL, stderr=subprocess.STDOUT)
                FNULL.close()
                os.rename(root_folder+'.tr', 'media/tmp/'+lang+'_'+ver+'.tr')
                shutil.rmtree(root_folder)
            else:
                return Response({"response": "nosource"}, status=403)
        
        source_file = open('media/tmp/'+lang+'_'+ver+'.tr', 'rb')
        response = HttpResponse(files.File(source_file), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="%s"' % (lang+'_'+ver+'.tr')
        source_file.close()
        return response

def index(request):
    take = Take.objects.all().last()
    return render(request, 'index.html', {"lasttake":take})

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
    
    res = takes.values()

    for take in res:
        dic = {}
        # Include language name
        dic["language"] = Language.objects.filter(pk=take["language_id"]).values()[0]
        # Include book name
        dic["book"] = Book.objects.filter(pk=take["book_id"]).values()[0]
        # Include author of file
        user = User.objects.filter(pk=take["user_id"])
        if user:
            dic["user"] = user.values()[0]

        # Include comments
        dic["comments"] = []
        for cmt in Comment.objects.filter(file=take["id"]).values():
            dic2 = {}
            dic2["comment"] = cmt
            # Include author of comment
            cuser = User.objects.filter(pk=cmt["user_id"])
            if cuser:
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
        slug = meta["slug"],
        defaults={'slug': meta['slug'], 'booknum': meta['book_number'], 'name': data['bookname']},
    )
    language, l_created = Language.objects.get_or_create(
        slug = meta["language"],
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
        with open ('language.json', 'rb') as fp:
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
