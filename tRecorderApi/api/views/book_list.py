from rest_framework import views, status
from rest_framework.parsers import JSONParser
import json
from api.models import Take, Language, Book
from rest_framework.response import Response
from operator import itemgetter

class getBooksView(views.APIView):
    parser_classes = (JSONParser,)

    def post(self, request):
        data = json.loads(request.body)
        allTakes = Take.objects.all().values()
        allTakes = allTakes.filter(is_source = False)
        books = []
        for take in allTakes:
            bo_oks = Book.objects.filter(id = take["book_id"]).values()
            bo_oks = list(bo_oks)
            if bo_oks[0]["slug"] not in books:
                books.append(bo_oks[0]["slug"])
        return Response(books, status = 200)
