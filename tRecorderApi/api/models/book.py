import json
from django.db import models
from django.forms.models import model_to_dict


class Book(models.Model):
    slug = models.CharField(max_length=3, unique=True, blank=True)
    name = models.CharField(max_length=100, blank=True)
    booknum = models.IntegerField(default=0)

    @staticmethod
    def getBooksList():
        lst = []
        projects = Project.objects.filter(is_source=False)
        for project in projects:
            if project.version and project.language and project.book:
                lst.append(model_to_dict(project.book))

        # distinct list
        lst = list({v['id']: v for v in lst}.values())
        return lst

    @staticmethod
    def getBookByCode(code):
        with open('books.json') as books_file:
            books = json.load(books_file)

        bn = ""
        for dicti in books:
            if dicti["slug"] == code:
                bn = dicti["name"]
                break
        return bn

    class Meta:
        ordering = ["booknum"]
        app_label = "api"

    def __unicode__(self):
        return self.name
