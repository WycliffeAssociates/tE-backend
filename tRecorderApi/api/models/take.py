from django.db import models
from django.utils.timezone import now
from django.contrib.contenttypes.fields import GenericRelation
from ..models import book, language, chunk, project, anthology, version, chapter, mode
import os
import json
#from .comment import Comment
Language = language.Language
Book = book.Book
Chunk = chunk.Chunk
Project = project.Project
Anthology= anthology.Anthology
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
    def saveTakesToDB(meta, relpath, data, published=False):
        # Create Language in database if it's not there
        language_obj, l_created = Language.objects.get_or_create(
            slug=meta["language"],
            defaults={
                'slug': meta['language'],
                'name': data['langname']},
        )
        #check if the anthology is in DB if not create it, returns a tuple with an instance of the object in DB and a boolean
        anthology_obj, a_created = Anthology.objects.get_or_create(
            slug=meta["anthology"],
            defaults={
                'slug': meta['anthology'],
                'name': ''                  #TODO add name after it is included in meta
            }
        )

        # Create Book in database if it's not there
        book_obj, b_created = Book.objects.get_or_create(
            slug=meta["slug"],
            defaults={
                'slug': meta['slug'],
                'number': meta['book_number'],
                'name': data['bookname'],
                'anthology': anthology_obj
            },

        )
        # Create version in database if it does not exist
        version_obj, v_created = Version.objects.get_or_create(
            slug=meta["version"],
            defaults={
                'slug': meta['version'],  #TODO add name and unit after it is included in meta
                'name': ''

            }
        )

        # Create mode in database if it does not exist
        mode_obj, m_created = Mode.objects.get_or_create(
            name=meta["mode"],
            defaults={
                'slug': '',            #TODO add slug after it is included in meta
                'name': meta['mode']
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
                'source_language': language_obj #TODO create source language
            },
        )


        # Create Chapter in database if it's not there
        chapter_obj, cr_created = Chapter.objects.get_or_create(
            project=project_obj,
            number=meta['chapter'],
            defaults={
                'number': meta['chapter'],
                'checked_level': 0,  # TODO get checked_level from tR
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
                'duration': data['duration'],
                'rating': 0,  # TODO get rating from tR
                'markers': markers,
            }
            try:
                obj = Take.objects.get(
                    chunk=chunk,
                )
                if os.path.exists(obj.location):
                    os.remove(obj.location)
                for key, value in defaults.items():
                    setattr(obj, key, value)
                obj.save()
            except Take.DoesNotExist:
                new_values = {
                    'chunk': chunk,
                }
                new_values.update(defaults)
                obj = Take(**new_values)
                obj.save()
            else:
                        take = Take(location=relpath,
                        duration=data['duration'],
                        rating=0,  # TODO get rating from tR
                        markers=markers,
                        user_id=1,
                        )  # TODO get author of file and save it to Take model
            take.save()

