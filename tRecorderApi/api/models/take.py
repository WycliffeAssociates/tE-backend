import json
import json
import os

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.timezone import now

from ..models import book, language, chunk, anthology, version, chapter, mode, project

Language = language.Language
Book = book.Book
Chunk = chunk.Chunk
Anthology = anthology.Anthology
Version = version.Version
Chapter = chapter.Chapter
Mode = mode.Mode
Project = project.Project


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

    def get_takes(chunk_id):
        takes = Take.objects.filter(id=chunk_id)
        ls = []
        for take in takes:
            tk = {
                "rating": take.rating,
                "published": take.published,
                "markers": take.markers,
                "location": take.location,
                "duration": take.duration,
                "id": take.id
            }
            ls.append(tk)
        return ls

    @staticmethod
    def saveTakesToDB(meta, relpath, take_data, manifest, published=False):
        try:
            # Create Language in database if it's not there
            language_obj, l_created = Language.objects.get_or_create(
                slug=manifest["language"]["slug"],
                defaults={
                    'slug': manifest["language"]["slug"],
                    'name': manifest["language"]["name"]},
            )
            # check if the anthology is in DB if not create it, returns a tuple with an instance of the object in DB and a boolean
            anthology_obj, a_created = Anthology.objects.get_or_create(
                slug=manifest["anthology"]["slug"],
                defaults={
                    'slug': manifest["anthology"]["slug"],
                    'name': manifest["anthology"]["name"]
                }
            )

            # Create Book in database if it's not there
            book_obj, b_created = Book.objects.get_or_create(
                slug=manifest["book"]["slug"],
                defaults={
                    'slug': manifest["book"]['slug'],
                    'number': manifest["book"]['number'],
                    'name': manifest["book"]['name'],
                    'anthology': anthology_obj
                },

            )
            # Create version in database if it does not exist
            version_obj, v_created = Version.objects.get_or_create(
                slug=manifest["version"]["slug"],
                defaults={
                    'slug': manifest["version"]["slug"],  # TODO add name and unit after it is included in meta
                    'name': manifest["version"]["name"]

                }
            )

            # Create mode in database if it does not exist
            mode_obj, m_created = Mode.objects.get_or_create(
                name=manifest["mode"]['name'],
                slug=manifest["mode"]['slug'],
                defaults={
                    'slug': manifest["mode"]["slug"],
                    'name': manifest["mode"]["name"]
                }
            )

            # Create Project in database if it's not there
            project_obj, p_created = Project.objects.get_or_create(
                version=version_obj,
                mode=mode_obj,
                anthology=anthology_obj,
                language=language_obj,
                book=book_obj,
                published=published,
                defaults={
                    'version': version_obj,
                    'mode': mode_obj,
                    'anthology': anthology_obj,
                    'language': language_obj,
                    'book': book_obj,
                    'published': published,
                    'source_language': language_obj
                },
            )

            manifest_chapter = int(meta['chapter']) - 1
            checked_level = manifest['manifest'][manifest_chapter]["checking_level"]

            # Create Chapter in database if it's not there
            chapter_obj, cr_created = Chapter.objects.get_or_create(
                project=project_obj,
                number=meta['chapter'],
                defaults={
                    'number': meta['chapter'],
                    'checked_level': checked_level,
                    'project': project_obj},
            )

            # Create Chunk in database if it's not there
            chunk_obj, ck_created = Chunk.objects.get_or_create(
                chapter=chapter_obj,
                startv=meta['startv'],
                endv=meta['endv'],
                defaults={
                    'startv': meta['startv'],
                    'endv': meta['endv'],
                    'chapter': chapter_obj},
            )

            markers = json.dumps(meta['markers'])

            # If the take came from .tr file (Source audio)
            # then check if it exists in database
            # if it exists then update its data
            # otherwise create new record
            # TODO remove source files functionality
            if published:
                defaults = {
                    'location': relpath,
                    'duration': take_data['duration'],
                    'rating': 0,  # TODO get rating from tR
                    'markers': markers,
                }
                try:
                    obj = Take.objects.get(
                        chunk=chunk_obj,
                    )
                    if os.path.exists(obj.location):
                        os.remove(obj.location)
                    for key, value in defaults.items():
                        setattr(obj, key, value)
                    obj.save()
                except Take.DoesNotExist:
                    new_values = {
                        'chunk': chunk_obj,
                    }
                    new_values.update(defaults)
                    obj = Take(**new_values)
                    obj.save()
            else:
                take = Take(location=relpath,
                            chunk=chunk_obj,
                            duration=take_data['duration'],
                            rating=0,  # TODO get rating from tR
                            markers=markers,
                            )  # TODO get author of file and save it to Take model
                take.save()

        except Exception as e:
            return str(e), 400

    def by_project_id(id):
        return Take.objects.filter(chunk__chapter__project=id)
