import json
import os
from django.db import models
from django.forms.models import model_to_dict



class Project(models.Model):
    version = models.CharField(max_length=3, blank=True)
    mode = models.CharField(max_length=10, blank=True)
    anthology = models.CharField(max_length=2, blank=True)
    is_source = models.BooleanField(default=False)
    is_publish = models.BooleanField(default=False)
    language = models.ForeignKey(
        Language, on_delete=models.CASCADE, null=True, blank=True)
    source_language = models.ForeignKey(
        Language, related_name="language_source", null=True, blank=True)
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, null=True, blank=True)

    @staticmethod
    def getProjects(data):
        lst = []
        filter = {}

        if "language" in data:
            filter["language__slug"] = data["language"]
        if "version" in data:
            filter["version"] = data["version"]
        if "book" in data:
            filter["book__slug"] = data["book"]
        if "is_publish" in data:
            filter["is_publish"] = data["is_publish"]

        filter["is_source"] = False
        projects = Project.objects.filter(**filter)

        for project in projects:
            if not project.version or not project.language or not project.book:
                continue

            dic = {}

            dic["id"] = project.id
            dic["version"] = project.version
            dic["is_publish"] = project.is_publish

            latest_take = Take.objects.filter(chunk__chapter__project=project) \
                .latest("date_modified")
            # Get contributors
            dic["contributors"] = []
            dic["date_modified"] = latest_take.date_modified
            availChunks = 0
            checklvl = 10
            chapters = project.chapter_set.all()
            for chapter in chapters:
                availChunks += 1
                if chapter.checked_level < checklvl:
                    checklvl = chapter.checked_level
                chunks = chapter.chunk_set.all()
                for chunk in chunks:
                    availChunks += 1
                    takes = chunk.take_set.all()
                    for take in takes:
                        try:
                            if take.user.name not in dic["contributors"]:
                                dic["contributors"].append(take.user.name)
                        except:
                            pass

            dic["checked_level"] = checklvl
            mode = project.mode
            bkname = project.book.slug
            chunkInfo = []
            for dirpath, dirnames, files in os.walk(os.path.abspath('static/chunks/')):
                if dirpath[-3:] == bkname:
                    for fname in os.listdir(dirpath):
                        f = open(os.path.join(dirpath, fname), "r")
                        sus = json.loads(f.read())
                        chunkInfo = sus
                    break
            totalChunk = float(len(chunkInfo))
            completed = int(round((availChunks / totalChunk) * 100))
            dic["completed"] = completed

            # Get language
            try:
                dic["language"] = model_to_dict(project.language,
                                                fields=["slug", "name"])
            except:
                pass

            # Get book
            try:
                dic["book"] = model_to_dict(project.book,
                                            fields=["booknum", "slug", "name"])
            except:
                pass

            lst.append(dic)

        return lst

    @staticmethod
    def getVersionsByProject():
        lst = []
        projects = Project.objects.filter(is_source=False)
        for project in projects:
            if project.version and project.language and project.book:
                lst.append(project.version)

        # distinct list
        lst = list(set(lst))
        return lst

    class Meta:
        ordering = ["language", "version", "book"]
        app_label = "api"

    def __unicode__(self):
        return '{}-{}-{} ({})'.format(self.language, self.version, self.book, self.id)
