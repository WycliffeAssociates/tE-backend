from django.db import models


class Chunk(models.Model):
    startv = models.IntegerField(default=0)
    endv = models.IntegerField(default=0)
    chapter = models.ForeignKey(
        "Chapter",
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["startv"]

    def __str__(self):
        return '{}:{}-{}'.format(
            Chapter.objects.get(pk=self.chapter).number,
            self.startv,
            self.endv
        )
