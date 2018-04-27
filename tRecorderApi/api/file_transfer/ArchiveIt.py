import zipfile
from .ArchiveProject import ArchiveProject


class ArchiveIt(ArchiveProject):
    def archive(self, root_dir, project_file, location_list, remove_dir, project, update_progress, task_args):
        with zipfile.ZipFile(project_file, 'w') as zipped_f:
            current_take = 0
            for file in location_list:
                zipped_f.write(file["conv"], file["conv"].replace(root_dir, ""))

                current_take += 1

                if project and update_progress and task_args:
                    # 3/3 of overall task
                    progress = int(((current_take / len(location_list) * 100) / 3) + ((100 / 3) * 2)) - 1

                    new_task_args = task_args + (progress, 100, 'Zipping takes...', {
                        'lang_slug': project["lang_slug"],
                        'lang_name': project["lang_name"],
                        'book_slug': project["book_slug"],
                        'book_name': project["book_name"],
                        'result': file["fn"]
                    })
                    update_progress(*new_task_args)

        remove_dir(root_dir)
        return project_file

    def extract(self):
        pass
