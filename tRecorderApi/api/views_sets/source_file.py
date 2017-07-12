from rest_framework import views, status
from rest_framework.parsers import JSONParser
from helpers import getTakesByProject
import time
import uuid
import os
import shutil
import pydub
import subprocess
from rest_framework.response import Response
from django.http import HttpResponse
from django.core import files
from rest_framework.parsers import JSONParser, FileUploadParser
from tinytag import TinyTag
import urllib2
import pickle


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

# class UploadSourceFileView(views_sets.APIView):
#     parser_classes = (FileUploadParser,)
#
#     def post(self, request, filename, format='tr'):
#         global uuid_name
#         if request.method == 'POST':
#             uuid_name = str(time.time()) + str(uuid.uuid4())
#             tempFolder = "media" + os.sep + "dump" + os.sep + uuid_name + os.sep
#             if not os.path.exists(tempFolder):
#                 os.makedirs(tempFolder)
#                 data = request.data['file']
#                 with open(tempFolder + os.sep + "source.tr", 'w') as temp_file:
#                     i = 0
#                     for line in data:
#                         if i > 3:
#                             temp_file.write(line)
#                         i += 1
#             else:
#                 print "error"
#         try:
#             FNULL = open(os.devnull, 'w')
#             subprocess.call(
#                 ['java', '-jar', 'aoh/aoh.jar', '-x', tempFolder + os.sep + "source.tr"],
#                 stdout=FNULL, stderr=subprocess.STDOUT)
#             os.remove(tempFolder + os.sep + "source.tr")
#             FNULL.close()
#             bookname = ''
#             bookcode = ''
#             langname = ''
#             langcode = ''
#
#             for root, dirs, files in os.walk(tempFolder):
#                 for f in files:
#                     abpath = os.path.join(root, os.path.basename(f))
#                     # abpath = os.path.abspath(os.path.join(root, f))
#                     try:
#                         meta = TinyTag.get(abpath)
#                     except LookupError:
#                         return Response({"response": "badwavefile"}, status=403)
#
#                     a = meta.artist
#                     lastindex = a.rfind("}") + 1
#                     substr = a[:lastindex]
#                     pls = json.loads(substr)
#
#                     if bookcode != pls['slug']:
#                         bookcode = pls['slug']
#                         bookname = getBookByCode(bookcode)
#                     if langcode != pls['language']:
#                         langcode = pls['language']
#                         langname = getLanguageByCode(langcode)
#
#                     data = {
#                         "langname": langname,
#                         "bookname": bookname,
#                         "duration": meta.duration
#                     }
#                     prepareDataToSave(pls, abpath, data, True)
#             return Response({"response": "ok"}, status=200)
#         except:
#             return Response({"response": "failed"}, status=403)
#         return Response(status=200)
#
#
# def getTakesByProject(data):
#     lst = []
#     takes = Take.objects
#     if "language" in data:
#         takes = takes.filter(language__slug=data["language"])
#     if "version" in data:
#         takes = takes.filter(version=data["version"])
#     if "book" in data:
#         takes = takes.filter(book__slug=data["book"])
#     if "chapter" in data:
#         takes = takes.filter(chapter=data["chapter"])
#     if "startv" in data:
#         takes = takes.filter(startv=data["startv"])
#     if "is_source" in data:
#         takes = takes.filter(is_source=data["is_source"])
#
#     res = takes.values()
#
#     for take in res:
#         dic = {}
#         # Include language name
#         lang = Language.objects.filter(pk=take["language_id"])
#         if lang and lang.count() > 0:
#             dic["language"] = lang.values()[0]
#         # Include book name
#         book = Book.objects.filter(pk=take["book_id"])
#         if book and book.count() > 0:
#             dic["book"] = book.values()[0]
#         # Include author of file
#         user = User.objects.filter(pk=take["user_id"])
#         if user and user.count() > 0:
#             dic["user"] = user.values()[0]
#
#         # Include comments
#         dic["comments"] = []
#         for cmt in Comment.objects.filter(file=take["id"]).values():
#             dic2 = {}
#             dic2["comment"] = cmt
#             # Include author of comment
#             cuser = User.objects.filter(pk=cmt["user_id"])
#             if cuser and cuser.count() > 0:
#                 dic2["user"] = cuser.values()[0]
#             dic["comments"].append(dic2)
#
#         # Parse markers
#         if take["markers"]:
#             take["markers"] = json.loads(take["markers"])
#         else:
#             take["markers"] = {}
#         dic["take"] = take
#         lst.append(dic)
#     return lst
#
#
# def prepareDataToSave(meta, abpath, data, is_source=False):
#     book, b_created = Book.objects.get_or_create(
#         slug=meta["slug"],
#         defaults={'slug': meta['slug'], 'booknum': meta['book_number'], 'name': data['bookname']},
#     )
#     language, l_created = Language.objects.get_or_create(
#         slug=meta["language"],
#         defaults={'slug': meta['language'], 'name': data['langname']},
#     )
#     markers = json.dumps(meta['markers'])
#     take = Take(location=abpath,
#                 duration=data['duration'],
#                 book=book,
#                 language=language,
#                 rating=0, checked_level=0,
#                 anthology=meta['anthology'],
#                 version=meta['version'],
#                 mode=meta['mode'],
#                 chapter=meta['chapter'],
#                 startv=meta[
#                     'startv'],
#                 endv=
#                 meta['endv'],
#                 markers=markers,
#                 user_id=1,
#                 is_source=is_source
#                 )
#     take.save()
#
#
# def getLanguageByCode(code):
#     url = 'http://td.unfoldingword.org/exports/langnames.json'
#     languages = []
#     try:
#         response = urllib2.urlopen(url)
#         languages = json.loads(response.read())
#         with open('language.json', 'wb') as fp:
#             pickle.dump(languages, fp)
#     except urllib2.URLError, e:
#         with open('language.json', 'rb') as fp:
#             languages = pickle.load(fp)
#
#     ln = ""
#     for dicti in languages:
#         if dicti["lc"] == code:
#             ln = dicti["ln"]
#             break
#     return ln
#
#
# def getBookByCode(code):
#     with open('books.json') as books_file:
#         books = json.load(books_file)
#
#     bn = ""
#     for dicti in books:
#         if dicti["slug"] == code:
#             bn = dicti["name"]
#             break
#     return bn
#
#
