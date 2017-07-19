from django.db import models


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

class Project(models.Model):
    version = models.CharField(max_length=3, blank=True)
    mode = models.CharField(max_length=10, blank=True)
    anthology = models.CharField(max_length=2, blank=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True, blank=True)
    source_language = models.ForeignKey(Language, related_name="language_source", null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ["language","version","book"]

    def __unicode__(self):
        return '{}-{}-{} ({})'.format(self.language, self.version, self.book, self.id)

class Chapter(models.Model):
    number = models.IntegerField(default=0)
    checked_level = models.IntegerField(default=0)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ["number"]

    def __unicode__(self):
        return self.number

class Chunk(models.Model):
    startv = models.IntegerField(default=0)
    endv = models.IntegerField(default=0)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ["startv"]

    def __unicode__(self):
        return "{}-{}".format(self.startv, self.endv)

class Take(models.Model):
    location = models.CharField(max_length=250)
    duration = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    #checked_level = models.IntegerField(default=0)
    #language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True, blank=True)
    #book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    #anthology = models.CharField(max_length=2, blank=True)
    #version = models.CharField(max_length=3, blank=True)
    #mode = models.CharField(max_length=10, blank=True)
    #startv = models.IntegerField(default=0)
    #endv = models.IntegerField(default=0)
    markers = models.TextField(null=True, blank=True)
    is_source = models.BooleanField(default=False)
    is_export = models.BooleanField(default=False)
    date_modified = models.DateTimeField(auto_now=True)
    #project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    #chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, null=True, blank=True)
    #source_language = models.ForeignKey(Language, related_name="language_source", null=True, blank=True)
    chunk = models.ForeignKey(Chunk, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ["chunk"]

    def __unicode__(self):
        return '{} ({})'.format(self.chunk, self.id)


class Comment(models.Model):
    location = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    take = models.ForeignKey(Take, on_delete=models.CASCADE, null=True, blank=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, null=True, blank=True)
    chunk = models.ForeignKey(Chunk, on_delete=models.CASCADE, null=True, blank=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.location
