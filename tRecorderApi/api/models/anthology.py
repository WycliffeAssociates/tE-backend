from django.db import models


class Anthology(models.Model):
    slug = models.CharField(unique=True, max_length=50)
    name = models.CharField(max_length=255)

    def get_anthology(anthology_slug=None):
        if(anthology_slug):
            return Anthology.objects.filter(slug__iexact=anthology_slug)
        return None

    def get_anthologies():
        return Anthology.objects.all()

    def __str__(self):
        return self.name