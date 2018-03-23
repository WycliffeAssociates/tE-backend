from django.http import JsonResponse

from ..file_transfer import FileUtility
from ..tasks import cleanup_orphan_files


def clean_orphans(request):
    task = cleanup_orphan_files.delay(FileUtility())
    return JsonResponse({"response": "processing", "task_id": task.id})
