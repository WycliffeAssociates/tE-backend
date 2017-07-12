import json
import pickle
import urllib2
import os
import hashlib
from api.models import Take, Language, Book, User, Comment

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