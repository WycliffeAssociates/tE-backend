from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from enum import Enum


class Language(models.Model):
    slug = models.CharField(max_length=20, unique=True, blank=True)
    name = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ["name"]

    def __unicode__(self):
        return self.name


class Book(models.Model):
    slug = models.CharField(max_length=3, unique=True, blank=True)
    name = models.CharField(max_length=100, blank=True)
    booknum = models.IntegerField(default=0)

    class Meta:
        ordering = ["booknum"]

    def __unicode__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=50)
    agreed = models.BooleanField()
    picture = models.CharField(max_length=250)

    class Meta:
        ordering = ["name"]

    def __unicode__(self):
        return self.name

class Comment(models.Model):   
    location = models.CharField(max_length=250)
    date_modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ["date_modified"]

    def __unicode__(self):
        return self.location

class Project(models.Model):
    version = models.CharField(max_length=3, blank=True)
    mode = models.CharField(max_length=10, blank=True)
    anthology = models.CharField(max_length=2, blank=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True, blank=True)
    source_language = models.ForeignKey(Language, related_name="language_source", null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    is_source = models.BooleanField(default=False)

    class Meta:
        ordering = ["language","version","book"]

    def __unicode__(self):
        return '{}-{}-{} ({})'.format(self.language, self.version, self.book, self.id)

class Chapter(models.Model):
    number = models.IntegerField(default=0)
    checked_level = models.IntegerField(default=0)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    is_publish = models.BooleanField(default=False)
    comments = GenericRelation(Comment)

    class Meta:
        ordering = ["number"]

    def __unicode__(self):
        return '{}'.format(self.number)

class Chunk(models.Model):
    startv = models.IntegerField(default=0)
    endv = models.IntegerField(default=0)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, null=True, blank=True)
    comments = GenericRelation(Comment)

    class Meta:
        ordering = ["startv"]

    def __unicode__(self):
        return '{}:{}-{}'.format(
            self.chapter.number, 
            self.startv, 
            self.endv)

class Take(models.Model):
    location = models.CharField(max_length=250)
    duration = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    markers = models.TextField(null=True, blank=True)   
    date_modified = models.DateTimeField(auto_now=True)
    chunk = models.ForeignKey(Chunk, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    comments = GenericRelation(Comment)

    class Meta:
        ordering = ["chunk"]

    def __unicode__(self):
        return '{} ({})'.format(self.chunk, self.id)
