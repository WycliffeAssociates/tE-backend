from django.db import models


class User(models.Model):
    name = models.CharField(max_length=50)
    agreed = models.BooleanField()
    picture = models.CharField(max_length=250)

    class Meta:
        ordering = ["name"]

    def __unicode__(self):
        return self.name
