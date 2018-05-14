import datetime

from api.file_transfer import FileUtility
from api.tasks import cleanup_orphan_files
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers


class CleanupOrphansView(generics.GenericAPIView):
    serializer_class = serializers.Serializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_data = {
            "icon_hash": request.user.icon_hash,
            "name_audio": request.user.name_audio
        }

        task = cleanup_orphan_files.delay(FileUtility(),
                                          title='Clean orphan files',
                                          started=datetime.datetime.now(),
                                          user=user_data)

        return Response({"response": "processing", "task_id": task.id}, status=202)
