from django.db import models


class Anthology(models.Model):
    slug = models.CharField(unique=True, max_length=50)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    @staticmethod
    def slug_by_id(id):
        anthology = Anthology.objects.filter(id=id).values('slug')[0]
        return anthology['slug']
