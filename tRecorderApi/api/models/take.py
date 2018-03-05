import json
import hashlib
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.timezone import now

from ..file_transfer.FileUtility import FileUtility
from ..models import book, language, chunk, anthology, version, chapter, mode
import os

Language = language.Language
Book = book.Book
Chunk = chunk.Chunk
Anthology = anthology.Anthology
Version = version.Version
Chapter = chapter.Chapter
Mode = mode.Mode


class Take(models.Model):
    location = models.CharField(max_length=255)
    duration = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    published = models.BooleanField(default=False)
    markers = models.TextField(blank=True)
    date_modified = models.DateTimeField(default=now)
    chunk = models.ForeignKey("Chunk", on_delete=models.CASCADE)
    comment = GenericRelation("Comment")

    class Meta:
        ordering = ["chunk"]

    def __str__(self):
        return '{} ({})'.format(self.chunk, self.id)

    @property
    def has_comment(self):
        return Take.objects.filter(comment__object_id=self.id).exists()

    @property
    def name(self):
        take = Take.objects.get(pk=self.id)
        return take.location.split(os.sep)[-1:][0]

    @property
    def md5hash(self):
        hash_md5 = hashlib.md5()
        take = Take.objects.get(pk=self.id)
        try:
            with open(take.location, "rb") as file:
                for chunk in iter(lambda: file.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except:
            return ""

    @staticmethod
    def import_takes(file_path, duration, markers, rating, chunk):
        take = Take(location=file_path,
                    chunk=chunk,
                    duration=duration,
                    rating=rating,
                    markers=markers,
                    )
        take.save()
