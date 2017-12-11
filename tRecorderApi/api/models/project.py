import json
import os
from django.db import models
from .take import Take
from .chapter import Chapter


class Project(models.Model):
    version = models.ForeignKey("Version")
    mode = models.ForeignKey("Mode", on_delete=models.CASCADE)
    anthology = models.ForeignKey("Anthology")
    language = models.ForeignKey("Language")
    source_language = models.ForeignKey(
        "Language",
        related_name="language_source",
        blank=True,
        null=True
    )
    book = models.ForeignKey("Book")
    published = models.BooleanField(default=False)

    class Meta:
        ordering = ["language", "version", "book"]
        unique_together = (("version", "anthology", "language", "mode", "book"),)

    def __str__(self):
        return '{}-{}-{} ({})'.format(self.language, self.version, self.book, self.id)

    @staticmethod
    def get_projects(projects):
        project_list = []
        for project in projects:
            dic = {"id": project.id,
                   "published": project.published,
                   "contributors": [],
                   "version": {
                       "slug": project.version.slug,
                       "name": project.version.name
                   },
                   "anthology": {
                       "slug": project.anthology.slug,
                       "name": project.anthology.name
                   },
                   "language": {
                       "slug": project.language.slug,
                       "name": project.language.name
                   },
                   "book": {
                       "slug": project.book.slug,
                       "name": project.book.name,
                       "number": project.book.number
                   }
                   }
            latest_take = Take.objects.filter(chunk__chapter__project=project) \
                .latest("date_modified")

            dic["date_modified"] = latest_take.date_modified

            min_check_level = Chapter.objects.all().values_list('checked_level') \
                .order_by('checked_level')[0][0]

            chunks_done = Chapter.objects.all().values_list('chunk').count()

            dic["checked_level"] = min_check_level

            book_name_slug = project.book.slug

            total_chunk = Project.get_total_chunks(book_name_slug)

            dic["completed"] = Project.get_percentage_completed(chunks_done, total_chunk)

            project_list.append(dic)

        return project_list

    @staticmethod
    def get_percentage_completed(chunks_done, total_chunks):
        return int(round((chunks_done / total_chunks) * 100))

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
