import json
import os

from django.db import models
from .chunk import Chunk


class Project(models.Model):
    version = models.ForeignKey("Version", on_delete=models.CASCADE)
    mode = models.ForeignKey("Mode", on_delete=models.CASCADE)
    anthology = models.ForeignKey("Anthology", on_delete=models.CASCADE)
    language = models.ForeignKey("Language", on_delete=models.CASCADE)
    source_language = models.ForeignKey(
        "Language",
        related_name="language_source",
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    published = models.BooleanField(default=False)

    class Meta:
        ordering = ["language", "version", "book"]
        unique_together = (
            ("version", "anthology", "language", "mode", "book"),)

    def __str__(self):
        return '{}-{}-{} ({})'.format(self.language, self.version, self.book, self.id)

    def get_completed_chunks(self):
        return Chunk.objects.filter(chapter__project=self.pk).count()

    @staticmethod
    def get_total_chunks(book_name_slug):
        chunk_info = []
        # TODO 'os' will not be useful when the code migrates to AWS
        for dirpath, dirnames, files in os.walk(os.path.abspath('static/chunks/')):
            if dirpath[-3:] == book_name_slug:
                for fname in os.listdir(dirpath):
                    f = open(os.path.join(dirpath, fname), "r")
                    sus = json.loads(f.read())
                    chunk_info = sus
                break
        return len(chunk_info)

    @property
    def completed(self):
        chunks_done = self.get_completed_chunks()
        total_chunks = self.get_total_chunks(self.book.slug)
        try:
            return int(round((chunks_done / total_chunks) * 100))
        except ZeroDivisionError:
            return 0

    @property
    def date_modified(self):
        from .take import Take
        take = Take.objects.filter(chunk__chapter__project=self.pk) \
            .order_by('date_modified') \
            .first()
        if take is not None:
            return take.date_modified
        else:
            return 0

    @staticmethod
    def import_project(version, mode, anthology, language, book, published=False):
        project_obj, p_created = Project.objects.get_or_create(
            version=version,
            mode=mode,
            anthology=anthology,
            language=language,
            book=book,
            defaults={
                'version': version,
                'mode': mode,
                'anthology': anthology,
                'language': language,
                'book': book,
                'published': published,
                'source_language': language
            }
        )
        return project_obj
