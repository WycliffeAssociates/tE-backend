import json

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.forms.models import model_to_dict

from .chapter import Chapter

from django.contrib.contenttypes.fields import GenericRelation


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
        return '{}:{}-{}'.format(
            Chapter.objects.get(pk=self.chapter).number,
            self.startv,
            self.endv
        )

    @staticmethod
    def create_chunk_filter(data):
        chunk_filter = {}
        if data is not None:
            if "project_id" in data:
                chunk_filter["chapter__project__id"] = data["project_id"]
            if "chapter_number" in data:
                chunk_filter["chapter__number"] = data["chapter_number"]
            # This is specific enough to grab chunks of a chapter, so return after
            if "project_id" in data and "chapter_number" in data:
                return chunk_filter

            if "anthology_slug" in data:
                chunk_filter["chapter__project__anthology__slug__iexact"] = data["anthology_slug"]
            if "language_slug" in data:
                chunk_filter["chapter__project__language__slug__iexact"] = data["language_slug"]
            if "book_slug" in data:
                chunk_filter["chapter__project__book__slug__iexact"] = data["book_slug"]
            if "version_slug" in data:
                chunk_filter["chapter__project__version__slug__iexact"] = data["version_slug"]
            return chunk_filter

    @staticmethod
    def get_chunks(data):
        chunk_filter = Chunk.create_chunk_filter(data)
        chunks = Chunk.fetch_data(chunk_filter)
        ls = []
        for chunk in chunks:
            ck = {"endv": chunk.endv, "startv": chunk.startv, "id": chunk.id}
            ls.append(ck)
        return ls

    @staticmethod
    def fetch_data(chunk_filter):
        if chunk_filter:
            return Chunk.objects.filter(**chunk_filter)

    @staticmethod
    def with_takes_by_project(data):
        data_dict = {}
        chunks_filter = Chunk.create_chunk_filter(data)
        if chunks_filter:

            chunks = Chunk.fetch_data(chunks_filter)

            data_dict["chunks"] = []

            for chunk in chunks:
                chunk_dict = {}

                # Include language data
                try:
                    if "language" not in data_dict:
                        data_dict["language"] = model_to_dict(chunk.chapter.project.language,
                                                              fields=["slug", "name"])
                except:
                    pass
                # Include book data
                try:
                    if "book" not in data_dict:
                        data_dict["book"] = model_to_dict(chunk.chapter.project.book, fields=["number", "slug", "name"])
                except:
                    pass

                # Include project data
                try:
                    if "project" not in data_dict:
                        data_dict["project"] = model_to_dict(chunk.chapter.project,
                                                             fields=["id", "published", "version", "mode", "anthology"])
                except:
                    pass

                # Include chapter data
                try:
                    if "chapter" not in data_dict:
                        data_dict["chapter"] = model_to_dict(chunk.chapter,
                                                             fields=["id", "published", "number", "checked_level",
                                                                     "comments"])

                        # Include comment for chapter
                        data_dict["chapter"]["comment"] = []
                        if chunk.chapter.comments:
                            for cmt in chunk.chapter.comments.all():
                                comm_dict = {}
                                comm_dict["comment"] = model_to_dict(cmt, fields=["id", "location", "date_modified"])
                                # Include author of comment
                                try:
                                    comm_dict["user"] = model_to_dict(cmt.user, fields=["name", "agreed", "picture"])
                                except Exception as e:
                                    print(e)
                                    pass
                                data_dict["chapter"]["comment"].append(comm_dict)
                except Exception as e:
                    print(e)
                    pass

                # Include comment for chunk
                chunk_dict["comments"] = []
                if chunk.comments:
                    comments = chunk.comments.all()
                    if comments:
                        for cmt in comments():
                            comm_dict = {}
                            comm_dict["comment"] = model_to_dict(cmt, fields=["id", "location", "date_modified"])
                            # Include author of comment
                            try:
                                comm_dict["user"] = model_to_dict(cmt.user, fields=["name", "agreed", "picture"])
                            except:
                                pass
                            chunk_dict["comments"].append(comm_dict)

                # Include takes
                takes_list = []
                for take in chunk.take_set.all():
                    if "published" in data:
                        if take.published != bool(data["published"]):
                            continue

                    take_dict = {}

                    # Include comment for chunks
                    take_dict["comment"] = []
                    if take.comment:
                        for cmt in take.comment.all():
                            comm_dict = {}
                            comm_dict["comment"] = model_to_dict(cmt, fields=["id", "location", "date_modified"])
                            # Include author of comment
                            try:
                                comm_dict["user"] = model_to_dict(cmt.user, fields=["name", "agreed", "picture"])
                            except:
                                pass
                            take_dict["comment"].append(comm_dict)

                        # Parse markers
                        if take.markers:
                            take.markers = json.loads(take.markers)
                        else:
                            take.markers = {}

                    take_dict["take"] = model_to_dict(take, fields=[
                        "location", "duration", "rating",
                        "markers", "id",
                        "published"
                    ])

                    takes_list.append(take_dict)

                chunk_dict["takes"] = takes_list

                chunk_dict2 = model_to_dict(chunk, fields=[
                    "startv", "endv", "id"
                ])

                chunk_dict = {**chunk_dict, **chunk_dict2}

                data_dict["chunks"].append(chunk_dict)
            return data_dict
        else:
            return None