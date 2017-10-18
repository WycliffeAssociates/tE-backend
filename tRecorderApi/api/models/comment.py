from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.timezone import now


class Comment(models.Model):
    location = models.CharField(max_length=250)
    date_modified = models.DateTimeField(default=now)
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, null=True, blank=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ["date_modified"]
        app_label = "api"

    def __unicode__(self):
        return self.location
