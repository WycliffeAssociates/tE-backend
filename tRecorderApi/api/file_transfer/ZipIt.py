from .ArchiveProject import ArchiveProject
import zipfile


class ZipIt(ArchiveProject):

    def archive(self):
        pass

    @staticmethod
    def extract(file, directory, update_progress, task_args):
        try:
            with zipfile.ZipFile(file, "r") as zip_file:
                takes = zip_file.infolist()
                current_take = 0

                for i, take in enumerate(takes):
                    zip_file.extract(take, directory)

                    current_take += 1

                    if update_progress and task_args:
                        # 1/2 of overall task
                        progress = int(((current_take / len(takes) * 100) / 2))

                        new_task_args = task_args + (progress, 100, 'Extracting takes...', {
                            'lang_slug': "--",
                            'lang_name': "--",
                            'book_slug': "--",
                            'book_name': "--",
                            'result': str(take.filename)
                        })
                        update_progress(*new_task_args)

            return 'ok', 200
        except zipfile.BadZipfile as e:
                return e, 400

