from api.file_transfer.ArchiveIt import ArchiveIt
from api.file_transfer.AudioUtility import AudioUtility
from api.file_transfer.Download import Download
from api.file_transfer.FileUtility import FileUtility

from api.models import Anthology
from api.models import Chunk
from api.models import Mode
from api.models import Version

from rest_framework import views
from rest_framework.parsers import JSONParser
from rest_framework.response import Response


class TrProjectFiles(views.APIView):
    parser_classes = (JSONParser,)

    def post(self, request):
        data = request.data
        chunk_list = Chunk.with_takes_by_project(data)
        if chunk_list is not None:
            if len(chunk_list["chunks"]) > 0:
                tr_it = Download(ArchiveIt(), AudioUtility(), FileUtility())

                root_folder = tr_it.file_utility.root_dir(['media', 'tmp'])

                lang = chunk_list['language']["slug"]
                version = chunk_list['project']['version']
                book = chunk_list['book']['slug']

                filename = lang + '_' + Version.slug_by_version_id(version) + '_' + book

                tr_it.file_utility.create_folder_path(root_folder, lang, Version.slug_by_version_id(version), book)
                try:
                    for chunk in chunk_list["chunks"]:
                        for take in chunk["takes"]:
                            chapter_folder = tr_it.file_utility.create_chapter_path(root_folder, lang, Version.slug_by_version_id(version), book,
                                                                                    str(
                                                                                        chunk_list['chapter'][
                                                                                            'number']).zfill(2))
                            file_path = tr_it.file_utility.copy_files(take['take']['location'], chapter_folder)
                            if file_path.endswith('.wav'):
                                file_path_mp3 = file_path.replace('.wav', '.mp3')
                                meta = {
                                    "anthology": Anthology.slug_by_id(chunk_list['project']["anthology"]),
                                    "language": chunk_list["language"]["slug"],
                                    "version": Version.slug_by_version_id(chunk_list['project']["version"]),
                                    "slug": chunk_list['book']["slug"],
                                    "book_number": str(chunk_list['book']["number"]).zfill(2),
                                    "mode": Mode.slug_by_id(chunk_list['project']["mode"]),
                                    "chapter": str(chunk_list["chapter"]['number']).zfill(2),
                                    "startv": chunk["startv"],
                                    "endv": chunk["endv"],
                                    "markers": take['take']["markers"]
                                }
                                something = tr_it.audio_utility.write_meta(file_path, file_path_mp3, meta)
                                tr_it.file_utility.remove_file(file_path)
                    tr_it.file_utility.compile_into_tr(root_folder)
                    filename = tr_it.file_utility.create_tr_path('media', 'tmp', filename)
                    tr_it.file_utility.rename(root_folder + ".tr", filename)
                    tr_it.file_utility.remove_dir(root_folder)
                except Exception as e:
                    return Response({"error": str(e)}, status=400)
            else:
                return Response({"response": "no_source_files"}, status=400)
        else:
            return Response({"response": "no_source_files"}, status=400)
        return Response({"location": tr_it.file_utility.relative_path(filename)}, status=200)


# code flow

"""
# checks if project in data
# checks if one of language,version,book is not in data
# returns Response("not_enough_parameters"), if any of the check is true
# create empty object(new_data)
# checks if data has project, if true sets project to new_data
# sets language,version,book,is_published=True to new_data object

//database
#Gets chunks


#checks the size of the chunk is >0
#if false,no_source_files
#constructs temp folder and filename
#loops through project to get chunks
#loops through chunk to get takes
#constructs chapter_folder, if does not exists,creates it
#copy take files to chapter_folder
#stores file_name and file_path in respective variables
#checks the extension of file,if ends with .wav repaces with .mp3
#constructs meta data
#writes meta data to file
#removes file


#uses java lib to bundle into tr file
#renames the folder to .tr
#returns location to .tr file
"""
