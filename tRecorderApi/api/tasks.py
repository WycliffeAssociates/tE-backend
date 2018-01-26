import os

from tRecorderApi.celery import app

from .file_transfer.tinytag import TinyTag


@app.task
def add(x, y):
    return x + y

@app.task
def extract_process_file(self, directory, file, takeDatabase, ext):
    resp, stat = self.archive_project.extract(file, directory)
    if resp == 'ok':
        resp, stat = self.file_utility.process_uploaded_takes(directory, self.takeDatabase, ext)
        return resp, stat

#
# @app.task
# def process_uploaded(curObj, languages, manifest, directory, Take, ext):
#     for root, dirs, files in os.walk(directory):
#         for f in files:
#             if f == "manifest.json":
#                 continue
#             abpath = os.path.join(root, os.path.basename(f))
#             relpath = curObj.relative_path(abpath)
#             try:
#                 meta = TinyTag.get(abpath)  # get metadata for every file
#             except LookupError as e:
#                 return {'error': 'bad_wave_file'}, 400
#
#             metadata, take_info = curObj.parse_metadata(meta, languages)
#
#             if metadata == 'bad meta':
#                 return metadata, take_info
#             # highPassFilter(abpath)
#             is_source_file = False
#             if ext == 'tr':
#                 is_source_file = True
#                 manifest = curObj.create_manifest(take_info, metadata)
#             Take.saveTakesToDB(take_info, relpath,
#                                metadata, manifest, is_source_file)
#
#     return 'ok', 200
