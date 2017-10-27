from django.db import models


class Anthology(models.Model):
    slug = models.CharField(unique=True, max_length=50)
    name = models.CharField(max_length=255)

    def get_anthologies(*anthology_slug):
        if(anthology_slug):
            return Anthology.objects.filter(anthology_slug__iexact=anthology_slug)
        return Anthology.objects.all() 

    def __str__(self):
        return self.name