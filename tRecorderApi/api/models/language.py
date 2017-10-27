from django.db import models

class Language(models.Model):
    
    slug = models.CharField(unique=True, max_length=50)
    name = models.CharField(max_length=255)

    @staticmethod
    def get_language(*language_slug):
        if(language_slug):
            return Language.objects.filter(language_slug__iexact=language_slug)
        return Language.objects.all()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
