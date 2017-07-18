import json
import pickle
import urllib2
import os
import hashlib
import zipfile

from api.models import Take, Language, Book, User, Comment
from django.forms.models import model_to_dict


def getTakesByProject(data):
    lst = []
    takes = Take.objects.all()

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
    if "is_export" in data:
        takes = takes.filter(is_export=data["is_export"])

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

        # Include source file if any
        #if take["is_source"] is False:
        if take["source_language_id"] and dic["book"]:
            s_lang = Language.objects.filter(pk=take["source_language_id"])
            if s_lang and s_lang.count() > 0:
                s_dic = {}
                s_dic["language"] = s_lang.values()[0] 
                
                s_take = Take.objects \
                    .filter(language__slug=s_dic["language"]["slug"]) \
                    .filter(version=take["version"]) \
                    .filter(book__slug=dic["book"]["slug"]) \
                    .filter(mode=take["mode"]) \
                    .filter(chapter=take["chapter"]) \
                    .filter(startv=take["startv"]) \
                    .filter(endv=take["endv"]) \
                    .filter(is_source=True)
                if s_take and s_take.count() > 0:
                    s_dic["take"] = s_take.values()
                    dic["source"] = s_dic

        lst.append(dic)
    return lst

def updateTakesByProject(data):
    lst = []
    filter = data["filter"]
    fields = data["fields"]

    takes = Take.objects
    if "language" in filter:
        takes = takes.filter(language__slug=filter["language"])
    if "version" in filter:
        takes = takes.filter(version=filter["version"])
    if "book" in filter:
        takes = takes.filter(book__slug=filter["book"])
    if "chapter" in filter:
        takes = takes.filter(chapter=filter["chapter"])
    if "startv" in filter:
        takes = takes.filter(startv=filter["startv"])
    if "is_source" in filter:
        takes = takes.filter(is_source=filter["is_source"])

    updated = takes.update(**fields)
    return updated

def prepareDataToSave(meta, abpath, data, is_source=False):
    dic = {}
    
    book, b_created = Book.objects.get_or_create(
        slug=meta["slug"],
        defaults={'slug': meta['slug'], 'booknum': meta['book_number'], 'name': data['bookname']},
    )
    dic["book"] = model_to_dict(book)

    language, l_created = Language.objects.get_or_create(
        slug=meta["language"],
        defaults={'slug': meta['language'], 'name': data['langname']},
    )
    dic["language"] = model_to_dict(language)

    markers = json.dumps(meta['markers'])

    # If the take came from .tr file (Source audio)
    # then check if it exists in database
    # if it exists then update it's data
    # otherwise create new record
    if (is_source):
        defaults = {
            'location': abpath,
            'duration': data['duration'],
            'rating': 0,
            'checked_level': 0,
            'markers': markers,
        }
        try:
            obj = Take.objects.get(
                language=language,
                version=meta['version'],
                book=book,
                mode=meta['mode'],
                chapter=meta['chapter'],
                startv=meta['startv'],
                endv=meta['endv'],
                is_source=True,
            )
            os.remove(obj.location)
            for key, value in defaults.items():
                setattr(obj, key, value)
            obj.save()
        except Take.DoesNotExist:
            new_values = {
                'language': language,
                'version': meta['version'],
                'book': book,
                'mode': meta['mode'],
                'chapter': meta['chapter'],
                'startv': meta['startv'],
                'endv': meta['endv'],
                'is_source': True,
            }
            new_values.update(defaults)
            obj = Take(**new_values)
            obj.save()
        #dic["take"] = model_to_dict(obj)
    else:
        take = Take(location=abpath,
                    duration=data['duration'],
                    book=book,
                    language=language,
                    rating=0,
                    checked_level=0,
                    anthology=meta['anthology'],
                    version=meta['version'],
                    mode=meta['mode'],
                    chapter=meta['chapter'],
                    startv=meta['startv'],
                    endv=meta['endv'],
                    markers=markers,
                    is_source=is_source,
                    user_id=1)  # TODO get author of file and save it to Take model
        take.save()
        #dic["take"] = model_to_dict(take)
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
