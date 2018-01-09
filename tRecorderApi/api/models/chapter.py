import json
import os

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.forms.models import model_to_dict
from django.contrib.contenttypes.fields import GenericRelation


class Chapter(models.Model):
    number = models.IntegerField(default=0)
    checked_level = models.IntegerField(default=0)
    published = models.BooleanField(default=False)
    has_comment = models.BooleanField(default=False)
    project = models.ForeignKey(
        "Project",
        on_delete=models.CASCADE
    )
    comments = GenericRelation("Comment")

    class Meta:
        ordering = ["number"]

    def __str__(self):
        return '{}'.format(self.number)

    @property
    def date_modified(self):
        # take = Take.objects.filter(project=self.project) \
        #     .order_by('date_modified') \
        #     .first()
        # if take is not None:
        #     return take.date_modified
        # else:
        return 0

    @property
    def contributors(self):
        return ""
