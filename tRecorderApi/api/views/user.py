from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password, check_password

from ..models.user import TeUser
from rest_framework import viewsets
from rest_framework import views
from ..serializers import UserSerializer
from rest_framework import generics, status


# class UserViewSet(viewsets.ModelViewSet):
#     """This class handles the http GET, PUT, PATCH, POST and DELETE requests."""
#     queryset = TeUser.objects.all()
#     serializer_class = UserSerializer


class CreateTeUserView(views.APIView):
    parser_classes = (JSONParser,)

    def post(self, request):
        data = request.data

        password = make_password("P@ssw0rd-22")

        user, created = TeUser.objects.get_or_create(username=data["iconHash"])
        if created:
            user.password = password
            user.save()

        token, created = Token.objects.get_or_create(user=user)

        return Response({"token": token.key, "user": user.username}, status=200)


class LoginTeUserView(views.APIView):
    parser_classes = (JSONParser,)

    def post(self, request):
        data = request.data

        user = TeUser.objects.filter(username=data["iconHash"]).first()

        if user and check_password("P@ssw0rd-22", user.password):
            token, created = Token.objects.get_or_create(user=user)

            return Response({"token": token.key, "user": user.username}, status=200)

        return Response({"error": "Wrong user or password"}, status=400)

