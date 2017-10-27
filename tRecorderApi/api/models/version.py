from django.db import models

class Version(models.Model):
    slug = models.CharField(unique=True, max_length=50)
    name = models.CharField(max_length=255)

    def get_versions(*version_slug):
        if(version_slug):
            return Version.objects.filter(version_slug__iexact=version_slug)
        return Version.objects.all()

    def __str__(self):
        return self.name