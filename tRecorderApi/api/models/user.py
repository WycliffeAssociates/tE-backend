from django.contrib.auth.models import AbstractUser
from django.db import models


class TeUser(AbstractUser):
    icon_hash = models.CharField(max_length=255)
    audio_name = models.CharField(max_length=255)
