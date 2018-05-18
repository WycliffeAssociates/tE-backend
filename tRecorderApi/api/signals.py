from django.db.models.signals import pre_delete
from django.dispatch import receiver
import os
import shutil

from api.models import Take, Comment, User


@receiver(pre_delete, sender=Take)
def delete_take(sender, instance, **kwargs):
    try:
        os.remove(instance.location)
    except OSError:
        pass

    # check if any files left in the take directory
    try:
        directory = os.path.dirname(instance.location)
        files_num = len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])

        # if there is only manifest file, remove the directory
        if files_num == 1 and os.path.isfile(os.path.join(directory, "manifest.json")):
            shutil.rmtree(directory)
    except OSError:
        pass


@receiver(pre_delete, sender=Comment)
def delete_comment(sender, instance, **kwargs):
    try:
        os.remove(instance.location)
    except OSError:
        pass


@receiver(pre_delete, sender=User)
def delete_user(sender, instance, **kwargs):

    # Remove name_audio file from the file system
    try:
        os.remove(instance.name_audio)
    except OSError:
        pass
