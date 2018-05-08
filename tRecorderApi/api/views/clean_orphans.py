import datetime

from django.http import JsonResponse

from api.file_transfer import FileUtility
from api.tasks import cleanup_orphan_files
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class CleanupOrphansView(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        task = cleanup_orphan_files.delay(FileUtility(),
                                             title='Clean orphan files',
                                             started=datetime.datetime.now(),
                                             user_icon_hash=request.user.icon_hash)

        return Response({"response": "processing", "task_id": task.id}, status=202)
