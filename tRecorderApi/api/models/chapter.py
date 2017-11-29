from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.forms.models import model_to_dict
from ..models import project
import os
import json
from django.contrib.contenttypes.fields import GenericRelation



class Chapter(models.Model):
    number = models.IntegerField(default=0)
    checked_level = models.IntegerField(default=0)
    published = models.BooleanField(default=False)
    project = models.ForeignKey(
        "Project",
        on_delete=models.CASCADE
    )
    comments = GenericRelation("Comment")

    class Meta:
        ordering = ["number"]

    def __str__(self):
        return '{}'.format(self.number)

    @staticmethod
    def getChaptersByProject(data):
        dic = {}
        filter = {}

        filter["language__slug"] = data["language"]
        filter["version__slug"] = data["version"]
        filter["book__slug"] = data["book"]
        filter["published"] = False
        from .project import Project
        projects = Project.objects.filter(**filter)

        for project in projects:
            # Get chapters

            if not project.version or not project.language or not project.book:
                continue

            mode = project.mode
            bkname = project.book.slug
            from.take import Take
            latest_take = Take.objects.filter(chunk__chapter__project=project) \
                .latest("date_modified")

            chaps = []
            chapters = project.chapter_set.all()
            for chapter in chapters:
                chap_dic = {}
                chap_dic["id"] = chapter.id
                chap_dic["chapter"] = chapter.number
                chap_dic["checked_level"] = chapter.checked_level
                chap_dic["published"] = chapter.published

                # contains information about all chunks in a book
                chunkInfo = []
                for dirpath, dirnames, files in os.walk(os.path.abspath('static/chunks')):
                    if dirpath[-3:] == bkname:
                        for fname in os.listdir(dirpath):
                            f = open(os.path.join(dirpath, fname), "r")
                            sus = json.loads(f.read())
                            chunkInfo = sus
                        break

                # contains info about relevant chapter
                chunkstuff = []
                chapnum = chapter.number
                for chunk in chunkInfo:
                    if chunk["id"][:2] == str("%02d" % chapnum):
                        chunkstuff.append(chunk)

                percentComplete = 0
                chunks = chapter.chunk_set.all()

                if len(chunkstuff) > 0:
                    if mode == "chunk":
                        percentComplete = int(round(len(chunks) / (len(chunkstuff)) * 100))
                    else:
                        versetotal = 0
                        for i in chunkstuff:
                            if int(i["lastvs"]) > versetotal:
                                versetotal = int(i["lastvs"])
                        if versetotal > 0:
                            percentComplete = int(round((len(chunks) / versetotal) * 100))

                chap_dic["percent_complete"] = percentComplete
                chap_dic["date_modified"] = latest_take.date_modified

                # Get contributors
                chap_dic["contributors"] = []
                for chunk in chunks:
                    takes = chunk.take_set.all()
                    for take in takes:
                        try:
                            if take.user.name not in chap_dic["contributors"]:
                                chap_dic["contributors"].append(take.user.name)
                        except:
                            pass

                # Get comments
                chap_dic["comments"] = []
                for cmt in chapter.comments.all():
                    dic2 = {}
                    dic2["comment"] = model_to_dict(cmt, fields=["location", "date_modified"])
                    # Include author of comment
                    try:
                        dic2["user"] = model_to_dict(cmt.user, fields=["name", "agreed", "picture"])
                    except:
                        pass
                    chap_dic["comments"].append(dic2)

                chaps.append(chap_dic)

            dic["chapters"] = chaps

            # Get language
            try:
                dic["language"] = model_to_dict(project.language,
                                                fields=["slug", "name"])
            except:
                dic["language"] = {}

            # Get book
            try:
                dic["book"] = model_to_dict(project.book,
                                            fields=["booknum", "slug", "name"])
            except:
                dic["language"] = {}
            # Get Project ID
            try:
                dic["project_id"] = project.id
            except:
                dic["project_id"] = {}
            # Get is_publish
            try:
                dic["published"] = project.is_publish
            except:
                dic["published"] = {}
        return dic
