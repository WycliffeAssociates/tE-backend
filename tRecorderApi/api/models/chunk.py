import json

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.forms.models import model_to_dict

from .chapter import Chapter


class Chunk(models.Model):
    startv = models.IntegerField(default=0)
    endv = models.IntegerField(default=0)
    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.CASCADE
    )
    comments = GenericRelation("Comment")

    class Meta:
        ordering = ["startv"]

    def __str__(self):
        return "{}"

    @property
    def has_comment(self):
        return Chunk.objects.filter(comments__object_id=self.id).exists()
