from django.db import models


class Language(models.Model):
    slug = models.CharField(unique=True, max_length=50)
    name = models.CharField(max_length=255)

    @staticmethod
    def get_language(slug):
        return Language.objects.filter(slug__iexact=slug)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
