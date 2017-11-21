from django.db import models


class Version(models.Model):
    slug = models.CharField(unique=True, max_length=50)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def slug_by_version_id(id):
        version= Version.objects.filter(id=id).values('slug')[0]
        return version['slug']
