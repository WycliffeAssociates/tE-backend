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
    else:
        self.file_utility.remove_file(file)
        logger.info("File extraction failed, so removed.")


@shared_task(name='download_project')
def download_project(self, takes, file_format):
    return self.file_utility.convert_and_compress(self, takes, file_format)
