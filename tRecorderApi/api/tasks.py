from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task(name='extract_and_save_project')
def extract_and_save_project(self, file, directory):
    resp, stat = self.archive_project.extract(file, directory)
    if resp == 'ok':
        self.file_utility.remove_file(file)
        logger.info("File extracted and  removed.")
        return self.file_utility.import_project(directory)
