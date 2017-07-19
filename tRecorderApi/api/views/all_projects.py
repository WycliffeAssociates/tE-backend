from rest_framework import views, status
from rest_framework.parsers import JSONParser
from api.models import Take, Language, Book, User, Comment
import json
from rest_framework.response import Response

class AllProjectsView(views.APIView):
    parser_classes = (JSONParser,)
    def post(self, request):
        allTakes = Take.objects.all().values()
        aVersion = []
        aBook = []
        authors = {}
        data = json.loads(request.body)
        convert_keys_to_string(data)
        #filters projects if needed
        if "version" in data:
            allTakes = allTakes.filter(version=data["version"])
        if "book" in data:
            allTakes = allTakes.filter(book__slug=data["book"])
        allTakes = allTakes.filter(is_source = False)
        for take in allTakes:
            if take["language_id"] not in aVersion:
                aVersion.append(take["language_id"])
            if take["book_id"] not in aBook:
                aBook.append(take["book_id"])
            tempAuthor = (take["language_id"], take["book_id"], str(take["version"]))
            if tempAuthor not in authors:
                authors[tempAuthor] = []
            authorName = User.objects.filter(id = take["user_id"]).values()
            authorName = list(authorName)
            if str(authorName[0]["name"]) not in authors[tempAuthor]:
                authors[tempAuthor].append(str(authorName[0]["name"]))
        if "language" in data:
            allLanguages = Language.objects.filter(slug = data["language"]).values()
        else:
            allLanguages = Language.objects.all().values()
        projects = []
        #loops through languages to find projects
        for lang in allLanguages:
            usedBooks = []
            usedVersion = []
            lang = dict(lang)
            takes = Take.objects.filter(language = lang['id']).values()
            takes = list(takes)
            #looks through takes to make sure Books/versions are correct
            for indTake in takes:
                if indTake["is_source"] == True:
                    continue
                else:
                    lan = {}
                    indTake = convert_keys_to_string(indTake)
                    if indTake["book_id"] not in usedBooks:
                        if indTake["book_id"] not in aBook:
                            continue
                        else:
                            spBook = Book.objects.filter(id = indTake["book_id"]).values()
                            lan["book"] = (spBook)
                            lan["lang"] = lang
                            lan["version"] = indTake["version"]
                            lan["timestamp"] = indTake["date_modified"]
                            lan["completed"] = 75
                            #future user = User.objects.filter(id = indTake["user"]).values()
                            tempAuthor = (indTake["language_id"], indTake["book_id"], str(indTake["version"]))
                            lan["contributors"] =  authors[tempAuthor]
                            usedBooks.append(indTake["book_id"])
                            usedVersion.append(indTake["version"])
                            projects.append(lan)
                    elif indTake["version"] not in usedVersion:
                        if indTake["version"] not in aVersion:
                            continue
                        else:
                            spBook = Book.objects.filter(id = indTake["book_id"]).values()
                            lan["book"] = (spBook)
                            lan["lang"] = lang
                            lan["version"] = indTake["version"]
                            lan["timestamp"] = indTake["date_modified"]
                            lan["completed"] = 75
                            #future user = User.objects.filter(id = indTake["user"]).values()
                            tempAuthor = (indTake["language_id"], indTake["book_id"], str(indTake["version"]))
                            lan["contributors"] =  authors[tempAuthor]
                            usedVersion.append(indTake["version"])
                            projects.append(lan)
                    else:
                        continue
        return Response(projects, status = 200)


def convert_keys_to_string(dictionary):
    """Recursively converts dictionary keys to strings."""
    if not isinstance(dictionary, dict):
        return dictionary
    return dict((str(k), convert_keys_to_string(v))
        for k, v in dictionary.items())
