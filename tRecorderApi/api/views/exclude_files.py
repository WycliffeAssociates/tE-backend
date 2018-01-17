from rest_framework import views, status
from rest_framework.parsers import JSONParser
import json
from .helpers import getFileName, md5Hash
from rest_framework.response import Response
from api.models import Take
from api.serializers import ExcludeFilesSerializer


class ExcludeFilesView(views.APIView):
    parser_classes = (JSONParser,)

    #The purpose of this request is to reduce the amount of unnecessary file uploads
    #during backup from translationRecorder
    def post(self, request):
        files_to_exclude = {}
        data = request.data
        #get the files associated with a particular project
        project = Take.objects.filter()
        for chunk in project["chunks"]:
            for take in chunk['takes']:
                location = take['take']['location']
                #for all files in the project, compute the md5 hash
                files_to_exclude[getFileName(location)] = md5Hash(location)
        #return the md5 hashes of files we have, so that duplicates can be avoided
        return Response(files_to_exclude, status=200)

    from api.models import Take
from rest_framework import viewsets
from api.serializers import TakeSerializer


class ExcludeFilesViewSet(viewsets.ReadOnlyModelViewSet):
    """This class handles the http GET, PUT, PATCH, POST and DELETE requests."""
    queryset = Take.objects.all()
    serializer_class = ExcludeFilesSerializer

    def build_params_filter(self, query):
        lang = query.get("lang", None)
        anth = query.get("anth", None)
        version = query.get("version", None)
        book = query.get("book", None)
        filter = {}
        if lang is not None:
            filter["chunk__chapter__project__lang__slug__iexact"] = lang
        if anth is not None:
            filter["chunk__chapter__project__anth__slug__iexact"] = anth
        if version is not None:
            filter["chunk__chapter__project__version__slug__iexact"] = version
        if book is not None:
            filter["chunk__chapter__project__book__slug__iexact"] = book
        return filter

    def get_queryset(self):
        queryset = Take.objects.all()
        if self.request.query_params:
            filter = self.build_params_filter(self.request.query_params)
            if filter:
                return queryset.filter(**filter)
            return None
        return queryset