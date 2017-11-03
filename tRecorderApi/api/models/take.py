from django.db import models
from django.utils.timezone import now


class Take(models.Model):
    location = models.CharField(max_length=255)
    duration = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    published = models.BooleanField(default=False)
    markers = models.TextField(blank=True)
    date_modified = models.DateTimeField(default=now)
    chunk = models.ForeignKey("Chunk", on_delete=models.CASCADE)

    class Meta:
        ordering = ["chunk"]

    def __str__(self):
        return '{} ({})'.format(self.chunk, self.id)

    # @staticmethod
    # def stitchSource(data):
    #     list = []
    #     filter = {}
    #     filter["chapter__project__language__slug"] = data["language"]
    #     filter["chapter__project__version"] = data["version"]
    #     filter["chapter__project__book__slug"] = data["book"]
    #     filter["chapter__number"] = data["chapter"]

    #     res = Chunk.objects.filter(**filter)
    #     return res

    # @staticmethod
    # def prepareDataToSave(meta, relpath, data, is_source=False):
    #     dic = {}

    # Create Language in database if it's not there
    #     language, l_created = Language.objects.get_or_create(
    #         slug=meta["language"],
    #         defaults={
    #             'slug': meta['language'],
    #             'name': data['langname']},
    #     )
    #     dic["language"] = model_to_dict(language)

    # Create Book in database if it's not there
    #     book, b_created = Book.objects.get_or_create(
    #         slug=meta["slug"],
    #         defaults={
    #             'slug': meta['slug'],
    #             'booknum': meta['book_number'],
    #             'name': data['bookname']},
    #     )
    #     dic["book"] = model_to_dict(book)

    # Create Project in database if it's not there
    #     project, p_created = Project.objects.get_or_create(
    #         version=meta["version"],
    #         mode=meta["mode"],
    #         anthology=meta["anthology"],
    #         language=language,
    #         book=book,
    #         is_source=is_source,
    #         defaults={
    #             'version': meta['version'],
    #             'mode': meta['mode'],
    #             'anthology': meta['anthology'],
    #             'language': language,
    #             'book': book,
    #             'is_source': is_source},
    #     )
    #     dic["project"] = model_to_dict(project)

    # Create Chapter in database if it's not there
    #     chapter, cr_created = Chapter.objects.get_or_create(
    #         project=project,
    #         number=meta['chapter'],
    #         defaults={
    #             'number': meta['chapter'],
    # 'checked_level': 0,  # TODO get checked_level from tR
    #             'project': project},
    #     )
    #     dic["chapter"] = model_to_dict(chapter)

    # Create Chunk in database if it's not there
    #     chunk, ck_created = Chunk.objects.get_or_create(
    #         chapter=chapter,
    #         startv=meta['startv'],
    #         endv=meta['endv'],
    #         defaults={
    #             'startv': meta['startv'],
    #             'endv': meta['endv'],
    #             'chapter': chapter},
    #     )
    #     dic["chunk"] = model_to_dict(chunk)

    #     markers = json.dumps(meta['markers'])

    # If the take came from .tr file (Source audio)
    # then check if it exists in database
    # if it exists then update it's data
    # otherwise create new record
    # TODO remove source files functionality
    #     if (is_source):
    #         defaults = {
    #             'location': relpath,
    #             'duration': data['duration'],
    # 'rating': 0,  # TODO get rating from tR
    #             'markers': markers,
    #         }
    #         try:
    #             obj = Take.objects.get(
    #                 chunk=chunk,
    #             )
    #             if os.path.exists(obj.location):
    #                 os.remove(obj.location)
    #             for key, value in defaults.items():
    #                 setattr(obj, key, value)
    #             obj.save()
    #         except Take.DoesNotExist:
    #             new_values = {
    #                 'chunk': chunk,
    #             }
    #             new_values.update(defaults)
    #             obj = Take(**new_values)
    #             obj.save()
    #     else:
    #         take = Take(location=relpath,
    #                     duration=data['duration'],
    # rating=0,  # TODO get rating from tR
    #                     markers=markers,
    #                     user_id=1,
    # chunk=chunk)  # TODO get author of file and save it to Take model
    #         take.save()
    #     return dic
