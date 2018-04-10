import json
import os
from io import BytesIO

from pydub import AudioSegment
from api.file_transfer import FileUtility


class AudioUtility:
    def high_pass_filter(self):
        pass

    def convert_to_mp3(self, root_directory, file_format):
        converted_mp3_list = []
        for subdir, dirs, files in os.walk(root_directory):
            for file in files:
                file_path = os.path.join(subdir, file)
                if file_format == 'mp3':
                    if file_path.endswith(".wav"):
                        sound = AudioSegment.from_wav(file_path)

                        filename = file_path.replace(".wav", ".mp3")

                        sound.export(filename, format="mp3")

                        # Add to array so it can be added to the archive
                        converted_mp3_list.append(filename)
                    else:
                        converted_mp3_list.append(filename)
                else:
                    converted_mp3_list.append(file_path)
        return converted_mp3_list

    def convert_in_memory(self, take, file_format):
        language_slug = take.chunk.chapter.project.language.slug
        book_slug = take.chunk.chapter.project.book.slug
        version_slug = take.chunk.chapter.project.version.slug

        if file_format == "mp3":
            filename = take.location.replace(".wav", ".mp3")
            path = os.path.join(
                language_slug,
                version_slug,
                book_slug,
                str(take.chunk.chapter).zfill(2),
                FileUtility.file_name(filename))

            sound = AudioSegment.from_wav(take.location)
            file_io = BytesIO()
            sound.export(file_io, format=file_format)

            return path, file_io.getvalue()
        else:
            with open(take.location, "rb") as take_contents:
                path = os.path.join(
                    language_slug,
                    version_slug,
                    book_slug,
                    str(take.chunk.chapter).zfill(2),
                    FileUtility.file_name(take.location))

                return path, take_contents.read()

    def write_meta(self, file_path, file_path_mp3, meta):
        sound = AudioSegment.from_wav(file_path)
        return sound.export(file_path_mp3, format='mp3', tags={'artist': json.dumps(meta)})
