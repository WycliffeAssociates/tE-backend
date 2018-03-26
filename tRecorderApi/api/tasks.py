import datetime
from time import sleep
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
                               'message': "{0!r}".format(exc),
                               'details': einfo,
                               'title': kwargs["title"],
                               'started': kwargs["started"],
                               'finished': datetime.datetime.now(),
                          })


@shared_task(name='extract_and_save_project', base=BaseTask)
def extract_and_save_project(self, file, directory, title, started):
    task = extract_and_save_project
    task.update_state(state='STARTED',
                      meta={
                          'name': task.name,
                          'title': title,
                          'started': started,
                          'message': "Extracting files..."
                      })

    resp, stat = self.archive_project.extract(file, directory)
    if resp == 'ok':
        self.file_utility.remove_file(file)
        logger.info("File extracted and removed.")
        return self.file_utility.import_project(directory, task, title, started)
    else:
        self.file_utility.remove_file(file)
        logger.info("File extraction failed, so removed.")

        raise BadZipfile(resp)


@shared_task(name='cleanup_orphan_files', base=BaseTask)
def cleanup_orphan_files(file_utility, title, started):
    task = cleanup_orphan_files
    task.update_state(state='STARTED',
                      meta={
                          'name': task.name,
                          'title': title,
                          'started': started,
                          'message': "Deleting orphan files..."
                      })

    files_removed = file_utility.cleanup_orphans()
    logger.info("{0} files have been removed".format(files_removed))
    return {
        'name': cleanup_orphan_files.name,
        'date': datetime.datetime.now(),
        'title': title,
        'message': "Cleaning files complete.",
        'details': "{0} files have been removed".format(files_removed),
        'started': started,
        'finished': datetime.datetime.now(),
    }


@shared_task(name='test_task', base=BaseTask)
def test_task(title, started):
    task = test_task
    task.update_state(state='STARTED',
                      meta={
                          'name': task.name,
                          'title': title,
                          'started': started,
                          'message': "Starting test task..."
                      })

    for counter in range(0, 6):
        if counter == 2:
            raise KeyError()
        test_task.update_state(state='PROGRESS',
                               meta={
                                   'current': counter * 5,
                                   'total': 60,
                                   'name': test_task.name,
                                   'started': started,
                                   'title': title,
                                   'message': 'Processing...'})
        sleep(5)

    return {
        'name': test_task.name,
        'started': started,
        'finished': datetime.datetime.now(),
        'title': title,
        'message': "Task complete!"}
