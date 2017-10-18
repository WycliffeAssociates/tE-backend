import json
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.forms.models import model_to_dict

class Chunk(models.Model):
    startv = models.IntegerField(default=0)
    endv = models.IntegerField(default=0)
    chapter = models.ForeignKey(
        Chapter, on_delete=models.CASCADE, null=True, blank=True)
    comments = GenericRelation(Comment)

    @staticmethod
    def getChunksWithTakesByProject(data):
        data_dic = {}
        chunks_list = []
        filter = {}

        if "project" in data:
            filter["chapter__project"] = data["project"]
        if "language" in data:
            filter["chapter__project__language__slug"] = data["language"]
        if "version" in data:
            filter["chapter__project__version"] = data["version"]
        if "book" in data:
            filter["chapter__project__book__slug"] = data["book"]
        if "mode" in data:
            filter["chapter__project__mode"] = data["mode"]
        if "chapter" in data:
            filter["chapter__number"] = data["chapter"]
        if "startv" in data:
            filter["startv"] = data["startv"]
        if "endv" in data:
            filter["endv"] = data["endv"]

        chunks = Chunk.objects.filter(**filter)

        data_dic["chunks"] = []

        for chunk in chunks:
            chunk_dic = {}

            # Include language data
            try:
                if "language" not in data_dic:
                    data_dic["language"] = model_to_dict(chunk.chapter.project.language,
                                                         fields=["slug", "name"])
            except:
                pass
            # Include book data
            try:
                if "book" not in data_dic:
                    data_dic["book"] = model_to_dict(chunk.chapter.project.book,
                                                     fields=["booknum", "slug", "name"])
            except:
                pass

            # Include project data
            try:
                if "project" not in data_dic:
                    data_dic["project"] = model_to_dict(chunk.chapter.project,
                                                        fields=["id", "is_publish", "version",
                                                                "mode", "anthology"])
            except:
                pass

            # Include chapter data
            try:
                if "chapter" not in data_dic:
                    data_dic["chapter"] = model_to_dict(chunk.chapter,
                                                        fields=["id", "is_publish", "number",
                                                                "checked_level", "comments"])

                    # Include comments for chapter
                    data_dic["chapter"]["comments"] = []
                    for cmt in chunk.chapter.comments.all():
                        comm_dic = {}
                        comm_dic["comment"] = model_to_dict(
                            cmt, fields=["id", "location", "date_modified"])
                        # Include author of comment
                        try:
                            comm_dic["user"] = model_to_dict(
                                cmt.user, fields=["name", "agreed", "picture"])
                        except:
                            pass
                        data_dic["chapter"]["comments"].append(comm_dic)
            except:
                pass

            # Include comments for chunk
            chunk_dic["comments"] = []
            for cmt in chunk.comments.all():
                comm_dic = {}
                comm_dic["comment"] = model_to_dict(
                    cmt, fields=["id", "location", "date_modified"])
                # Include author of comment
                try:
                    comm_dic["user"] = model_to_dict(
                        cmt.user, fields=["name", "agreed", "picture"])
                except:
                    pass
                chunk_dic["comments"].append(comm_dic)

            # Include source file if any / TODO remove source from code and db
            """source_language = chunk.chapter.project.source_language
            if source_language and chunk.chapter.project.book:
                source_dic = {}
                source_dic["language"] = model_to_dict(source_language, fields=["slug","name"])

                source_take = Take.objects \
                    .filter(chunk__chapter__project__language__slug=source_dic["language"]["slug"]) \
                    .filter(chunk__chapter__project__version=data_dic["project"]["version"]) \
                    .filter(chunk__chapter__project__book__slug=data_dic["book"]["slug"]) \
                    .filter(chunk__chapter__project__mode=data_dic["project"]["mode"]) \
                    .filter(chunk__chapter__number=data_dic["chapter"]["number"]) \
                    .filter(chunk__startv=chunk.startv) \
                    .filter(chunk__endv=chunk.endv) \
                    .filter(chunk__chapter__project__is_source=True) \
                    .first()
                if source_take:
                    if source_take.markers:
                        source_take.markers = json.loads(source_take.markers)
                    else:
                        source_take.markers = {}

                    source_dic["take"] = model_to_dict(source_take, fields=[
                        "markers","location","id"
                    ])
                    source_dic["take"]["version"] = source_take.chunk.chapter.project.version
                    chunk_dic["source"] = source_dic"""

            # Include takes
            takes_list = []
            for take in chunk.take_set.all():
                if "is_publish" in data:
                    if take.is_publish != data["is_publish"]:
                        continue

                take_dic = {}

                # Include author of file
                try:
                    take_dic["user"] = model_to_dict(
                        take.user, fields=["name", "agreed", "picture"])
                except:
                    pass

                # Include comments for chunks
                take_dic["comments"] = []
                # for cmt in Comment.objects.filter(content_type=take.id).values():
                for cmt in take.comments.all():
                    comm_dic = {}
                    comm_dic["comment"] = model_to_dict(
                        cmt, fields=["id", "location", "date_modified"])
                    # Include author of comment
                    try:
                        comm_dic["user"] = model_to_dict(
                            cmt.user, fields=["name", "agreed", "picture"])
                    except:
                        pass
                    take_dic["comments"].append(comm_dic)

                # Parse markers
                if take.markers:
                    take.markers = json.loads(take.markers)
                else:
                    take.markers = {}

                take_dic["take"] = model_to_dict(take, fields=[
                    "location", "duration", "rating",
                    "date_modified", "markers", "id",
                    "is_publish"
                ])

                takes_list.append(take_dic)

            chunk_dic["takes"] = takes_list

            chunk_dic2 = model_to_dict(chunk, fields=[
                "startv", "endv", "id"
            ])

            chunk_dic = dict(chunk_dic.items() + chunk_dic2.items())

            data_dic["chunks"].append(chunk_dic)
        return data_dic

    class Meta:
        ordering = ["startv"]
        app_label = "api"

    def __unicode__(self):
        return '{}:{}-{}'.format(
            self.chapter.number,
            self.startv,
            self.endv)
