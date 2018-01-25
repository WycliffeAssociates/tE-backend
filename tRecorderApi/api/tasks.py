from tRecorderApi.celery import app
import zipfile


@app.task()
def add(x, y):
    return x + y


@app.task
def extract(file, directory):
    try:
        zip_file = zipfile.ZipFile(file)
        zip_file.extractall(directory)
        zip_file.close()
        return 'ok', 200
    except zipfile.BadZipfile:
        return "bad zip file", 400
