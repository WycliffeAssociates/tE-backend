from tRecorderApi.celery import app


@app.task
def add(x, y):
    return x + y


@app.task(name='get_project')
def get_project(self,file, directory):
    resp, stat = self.archive_project.extract(file, directory)
    if resp == 'ok':
        return self.file_utility.import_project(directory)
