from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.timezone import now


class Comment(models.Model):
    location = models.CharField(max_length=255)
    date_modified = models.DateTimeField(default=now)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ["date_modified"]

    def __str__(self):
        return self.location

    @staticmethod
    def get_comments(data):
        commented_object = None
        if "chunk_id" in data:
             commented_object = Chunk.objects.get(id=data["chunk_id"])
        elif "take_id" in data:
            commented_object = Take.objects.get(id=data["take_id"])
        elif "chapter_id" in data:
            commented_object = Chapter.objects.get(id=data["chapter_id"])
        comments = commented_object.comments.all()
        status =  200 if len(comments) > 0 else 401
        result = None if comments is None else CommentSerializer(comments, many=true).data
        return result, status

