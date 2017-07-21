import json
import pickle
import urllib2
import os
import hashlib
import zipfile
from pydub import AudioSegment, effects
from django.db.models import Prefetch

from api.models import Take, Language, Book, User, Comment, Project, Chapter, Chunk
from django.forms.models import model_to_dict


def getTakesByProject(data):
    lst = []
    filter = {}
    takes = Take.objects.all()

    if "language" in data:
        filter["chunk__chapter__project__language__slug"] = data["language"]
    if "version" in data:
        filter["chunk__chapter__project__version"] = data["version"]
    if "book" in data:
        filter["chunk__chapter__project__book__slug"] = data["book"]
    if "chapter" in data:
        filter["chunk__chapter__number"] = data["chapter"]
    if "startv" in data:
        filter["chunk__startv"] = data["startv"]
    if "is_source" in data:
        filter["chunk__chapter__project__is_source"] = data["is_source"]
    if "is_publish" in data:
        filter["chunk__chapter__is_publish"] = data["is_publish"]

    res = takes.filter(**filter)
       
    for take in res:
        dic = {}
        # Include language name
        try:
            dic["language"] = model_to_dict(take.chunk.chapter.project.language, 
                fields=["slug","name"])
        except:
            pass
        # Include book name
        try:
            dic["book"] = model_to_dict(take.chunk.chapter.project.book, 
                fields=["booknum","slug","name"])
        except:
            pass
        # Include author of file
        try:
            dic["user"] = model_to_dict(take.user, fields=["name","agreed","picture"])
        except:
            pass
            

        # Include comments
        dic["comments"] = []
        #for cmt in Comment.objects.filter(content_type=take.id).values():
        for cmt in take.comments.all():
            dic2 = {}
            dic2["comment"] = model_to_dict(cmt, fields=["location","date"])
            # Include author of comment
            try:
                dic2["user"] = model_to_dict(cmt.user, fields=["name","agreed","picture"])
            except:
                pass
            dic["comments"].append(dic2)

        # Parse markers
        if take.markers:
            take.markers = json.loads(take.markers)
        else:
            take.markers = {}

        dic["take"] = model_to_dict(take, fields=[
            "location","duration","rating",
            "date_modified","markers"
        ])
        dic["take"]["anthology"] = take.chunk.chapter.project.anthology
        dic["take"]["version"] = take.chunk.chapter.project.version
        dic["take"]["chapter"] = take.chunk.chapter.number
        dic["take"]["mode"] = take.chunk.chapter.project.mode
        dic["take"]["startv"] = take.chunk.startv
        dic["take"]["endv"] = take.chunk.endv

        # Include source file if any
        #if take["is_source"] is False:
        source_language = take.chunk.chapter.project.source_language
        if source_language and take.chunk.chapter.project.book:
            s_dic = {}
            s_dic["language"] = model_to_dict(source_language, fields=["slug","name"])
            
            s_take = Take.objects \
                .filter(chunk__chapter__project__language__slug=s_dic["language"]["slug"]) \
                .filter(chunk__chapter__project__version=dic["take"]["version"]) \
                .filter(chunk__chapter__project__book__slug=dic["book"]["slug"]) \
                .filter(chunk__chapter__project__mode=dic["take"]["mode"]) \
                .filter(chunk__chapter__number=dic["take"]["chapter"]) \
                .filter(chunk__startv=dic["take"]["startv"]) \
                .filter(chunk__endv=dic["take"]["endv"]) \
                .filter(chunk__chapter__project__is_source=True) \
                .first()
            if s_take:
                if s_take.markers:
                    s_take.markers = json.loads(s_take.markers)
                else:
                    s_take.markers = {}

                s_dic["take"] = model_to_dict(s_take, fields=[
                    "markers","location"
                ])
                s_dic["take"]["version"] = s_take.chunk.chapter.project.version
                dic["source"] = s_dic

        lst.append(dic)
    return lst

def getProjects(data):
    lst = []
    filter = {}

    if "language" in data:
        filter["language__slug"] = data["language"]
    if "version" in data:
        filter["version"] = data["version"]
    if "book" in data:
        filter["book__slug"] = data["book"]

    filter["is_source"] = False
    projects = Project.objects.filter(**filter)

    for project in projects:
        dic = {}
        
        dic["version"] = project.version

        # Get contributors        
        dic["contributors"] = []
        chapters = project.chapter_set.all()
        for chapter in chapters:
            chunks = chapter.chunk_set.all()
            for chunk in chunks:
                takes = chunk.take_set.all()
                for take in takes:
                    if take.user.name not in dic["contributors"]:
                        dic["contributors"].append(take.user.name)
                            
        dic["completed"] = 75

        # Get language
        try:
            dic["language"] = model_to_dict(project.language, 
                fields=["slug","name"])
        except:
            pass

        # Get book
        try:
            dic["book"] = model_to_dict(project.book, 
                fields=["booknum","slug","name"])
        except:
            pass

        lst.append(dic)

    return lst

def updateTakesByProject(data):
    lst = []
    filter = {}
    fields = data["fields"]

    if "language" in data["filter"]:
        filter["chunk__chapter__project__language__slug"] = data["filter"]["language"]
    if "version" in data["filter"]:
        filter["chunk__chapter__project__version"] = data["filter"]["version"]
    if "book" in data["filter"]:
        filter["chunk__chapter__project__book__slug"] = data["filter"]["book"]
    if "chapter" in data["filter"]:
        filter["chunk__chapter__number"] = data["filter"]["chapter"]
    if "startv" in data["filter"]:
        filter["chunk__startv"] = data["filter"]["startv"]
    if "is_source" in data["filter"]:
        filter["chunk__chapter__project__is_source"] = data["filter"]["is_source"]
    if "is_publish" in data["filter"]:
        filter["chunk__chapter__is_publish"] = data["filter"]["is_publish"]

    return Take.objects.filter(**filter).update(**fields)

def prepareDataToSave(meta, abpath, data, is_source=False):
    dic = {}
    
    # Create Language in database if it's not there
    language, l_created = Language.objects.get_or_create(
        slug=meta["language"],
        defaults={
            'slug': meta['language'], 
            'name': data['langname']},
    )
    dic["language"] = model_to_dict(language)

    # Create Book in database if it's not there
    book, b_created = Book.objects.get_or_create(
        slug=meta["slug"],
        defaults={
            'slug': meta['slug'], 
            'booknum': meta['book_number'], 
            'name': data['bookname']},
    )
    dic["book"] = model_to_dict(book)

    # Create Project in database if it's not there
    project, p_created = Project.objects.get_or_create(
        version=meta["version"],
        mode=meta["mode"],
        anthology=meta["anthology"],
        language=language,
        book=book,
        is_source=is_source,
        defaults={
            'version': meta['version'], 
            'mode': meta['mode'], 
            'anthology': meta['anthology'],
            'language': language,
            'book': book,
            'is_source': is_source},
    )
    dic["project"] = model_to_dict(project)

    # Create Chapter in database if it's not there
    chapter, cr_created = Chapter.objects.get_or_create(
        project=project,
        number=meta['chapter'],
        defaults={
            'number': meta['chapter'], 
            'checked_level': 0,  #TODO get checked_level from tR
            'project': project},
    )
    dic["chapter"] = model_to_dict(chapter)

    # Create Chunk in database if it's not there
    chunk, ck_created = Chunk.objects.get_or_create(
        chapter=chapter,
        startv=meta['startv'],
        endv=meta['endv'],
        defaults={
            'startv': meta['startv'], 
            'endv': meta['endv'],
            'chapter': chapter},
    )
    dic["chunk"] = model_to_dict(chunk)

    markers = json.dumps(meta['markers'])

    # If the take came from .tr file (Source audio)
    # then check if it exists in database
    # if it exists then update it's data
    # otherwise create new record
    if (is_source):
        defaults = {
            'location': abpath,
            'duration': data['duration'],
            'rating': 0,  # TODO get rating from tR
            'markers': markers,
        }
        try:
            obj = Take.objects.get(
                chunk=chunk,
            )
            os.remove(obj.location)
            for key, value in defaults.items():
                setattr(obj, key, value)
            obj.save()
        except Take.DoesNotExist:
            new_values = {
                'chunk': chunk,
            }
            new_values.update(defaults)
            obj = Take(**new_values)
            obj.save()
    else:
        take = Take(location=abpath,
                    duration=data['duration'],
                    rating=0,  # TODO get rating from tR
                    markers=markers,
                    user_id=1,
                    chunk=chunk)  # TODO get author of file and save it to Take model
        take.save()
    return dic


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


def getFilePath(location):
    list = location.split(os.sep)[3:]
    return "/".join(list)


def highPassFilter(location):
    song = AudioSegment.from_wav(location)
    new = song.high_pass_filter(80)
    new.export(location, format = "wav")