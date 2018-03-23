import datetime
from zipfile import BadZipfile

import celery
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


class BaseTask(celery.Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        self.update_state(state='FAILURE',
                          meta={
                               'name': self.name,
                               'title': 'An error occurred',
                               'message': "{0!r}".format(exc),
                               'details': einfo,
                               'finished_at': datetime.datetime.now(),
                          })


@shared_task(name='extract_and_save_project', base=BaseTask)
def extract_and_save_project(self, file, directory):
    started_at = datetime.datetime.now()
    task = extract_and_save_project
    task.update_state(state='STARTED',
                      meta={
                          'name': task.name,
                          'started_at': started_at,
                          'message': "Extracting files..."
                      })

    resp, stat = self.archive_project.extract(file, directory)
    if resp == 'ok':
        self.file_utility.remove_file(file)
        logger.info("File extracted and removed.")
        return self.file_utility.import_project(task, started_at, directory)
    else:
        self.file_utility.remove_file(file)
        logger.info("File extraction failed, so removed.")

        raise BadZipfile(resp)


@shared_task(name='cleanup_orphan_files', base=BaseTask)
def cleanup_orphan_files(file_utility):
    started_at = datetime.datetime.now()
    task = cleanup_orphan_files
    task.update_state(state='STARTED',
                      meta={
                          'name': task.name,
                          'started_at': started_at,
                          'message': "Deleting orphan files..."
                      })

    files_removed = file_utility.cleanup_orphans()
    logger.info("{0} files have been removed".format(files_removed))
    return {
        'name': cleanup_orphan_files.name,
        'date': datetime.datetime.now(),
        'title': 'Cleaning orphan files',
        'message': "Cleaning files complete.",
        'details': "{0} files have been removed".format(files_removed),
        'started_at': started_at,
        'finished_at': datetime.datetime.now(),
    }
