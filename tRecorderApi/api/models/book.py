from django.db import models


class Book(models.Model):
    anthology = models.ForeignKey("Anthology", on_delete=models.CASCADE)
    slug = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    number = models.IntegerField(default=0)

    class Meta:
        ordering = ["number"]
        unique_together = ("anthology", "slug")

    def __str__(self):
        return self.name

