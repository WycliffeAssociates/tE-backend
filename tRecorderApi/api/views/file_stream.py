from rest_framework import views
import pydub
from django.http import StreamingHttpResponse

class FileStreamView(views.APIView):
    def get(self, request, filepath, format='mp3'):
        if filepath.endswith(".wav"):
            sound = pydub.AudioSegment.from_wav(filepath)
            file = sound.export()
        else:
            file = open(filepath, "rb")
        return StreamingHttpResponse(file)