from api.models import Anthology
from rest_framework import viewsets
from api.serializers import AnthologySerializer

class AnthologyViewSet(viewsets.ModelViewSet):
    """This class handles the http GET, PUT, PATCH, POST and DELETE requests."""
    queryset = Anthology.objects.all()
    serializer_class = AnthologySerializer