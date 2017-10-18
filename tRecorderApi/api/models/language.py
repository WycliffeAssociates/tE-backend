import urllib2
import pickle
import json
from django.db import models
from django.forms.models import model_to_dict


class Language(models.Model):
    slug = models.CharField(max_length=20, unique=True, blank=True)
    name = models.CharField(max_length=100, blank=True)

    @staticmethod
    def getLanguagesList():
        lst = []
        projects = Project.objects.filter(is_source=False)
        for project in projects:
            if project.version and project.language and project.book:
                lst.append(model_to_dict(project.language))

        # distinct list
        lst = list({v['id']: v for v in lst}.values())
        return lst

    @staticmethod
    def getLanguageByCode(code):
        url = 'http://td.unfoldingword.org/exports/langnames.json'
        languages = []
        try:
            response = urllib2.urlopen(url)
            languages = json.loads(response.read())
            with open('language.json', 'wb') as fp:
                pickle.dump(languages, fp)
        except urllib2.URLError:
            with open('language.json', 'rb') as fp:
                languages = pickle.load(fp)

        ln = ""
        for dicti in languages:
            if dicti["lc"] == code:
                ln = dicti["ln"]
                break
        return ln

    class Meta:
        ordering = ["name"]
        app_label = "api"

    def __unicode__(self):
        return self.name
