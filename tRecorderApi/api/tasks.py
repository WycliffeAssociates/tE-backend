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


@shared_task(name='cleanup_orphan_files')
def cleanup_orphan_files(res, self):
    files_removed = self.file_utility.cleanup_orphans()
    logger.info("{0} files have been removed".format(files_removed))
    return "{0} files have been removed".format(files_removed)
