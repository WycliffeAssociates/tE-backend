"""
    This module contains the suite of tests for testing the import_project()
    function found in the FileUtility class of the
    api.file_transfer.FileUtility module. The MOCKFILECONTENTS var is a
    constant defined in the api.tests.mock_manifest module which cotnains
    long-winded values tha are used inside this test.
"""
from unittest.mock import patch, Mock
from django.test import TestCase
from api.file_transfer import FileUtility

class FileUtilityTest(TestCase):
    """
        Test case for testing the behavior of the import_project() function
    """
    # This would be a mocked out version of the update progress function, which
    # is alright since we are not focusing on testing this function here.
    def mock_progress(self, task):
        print("running mock progress.\n")
        return True

    @patch('api.models.language.Language')
    @patch('api.models.anthology.Anthology')
    @patch('api.models.book.Book')
    @patch('api.models.version.Version')
    @patch('api.models.mode.Mode')
    @patch('api.models.project.Project')
    @patch('api.models.chapter.Chapter')
    @patch('api.models.chunk.Chunk')
    @patch('api.models.take.Take')
    @patch('api.models.comment.Comment')
    @patch('api.file_transfer.tinytag.TinyTag')
    @patch('api.tasks.update_progress', side_effect=mock_progress)
    @patch('api.file_transfer.FileUtility')
    @patch('api.file_transfer.os.path')
    def test_import_project(
            self,
            mock_path,
            mock_file_utility,
            mock_progress,
            mock_tiny_tag,
            mock_comment,
            mock_take,
            mock_chunk,
            mock_chapter,
            mock_project,
            mock_mode,
            mock_version,
            mock_book,
            mock_anthology,
            mock_language):
        """
            Test to verify that when an object of type FileUtility calls its
            import_project() method that it will return a json. FileUtility is
            mocked here so that we can predefine its other methods without actually
            calling it.
        """

        # Build Dependencies; in its entirety we are mocking a project for the
        #                     book of Joshua
        # Language
        mock_language.slug = 'en'
        mock_language.name = 'English'
        mock_language.import_language.return_value = mock_language

        #Antholgoy
        mock_anthology.slug = 'ot'
        mock_anthology.name = 'old testament'
        mock_anthology.import_anthology.return_value = mock_anthology

        # Book
        mock_book.anthology = mock_anthology
        mock_book.slug = 'jos'
        mock_book.name = 'Joshua'
        mock_book.number = 6
        mock_book.import_book.return_value = mock_book

        # Version
        mock_version.slug = 'ulb'
        mock_version.name = 'unlocked literal bible'
        mock_version.import_version.return_value = mock_version

        # Mode
        mock_mode.slug = 'chunk'
        mock_mode.name = 'chunk'
        mock_mode.unit = 'MULTI'
        mock_mode.import_mode.return_value = mock_mode

        #Project
        mock_project.id = 1
        mock_project.version = mock_version
        mock_project.mode = mock_mode
        mock_project.anthology = mock_anthology
        mock_project.language = mock_language
        mock_project.book = mock_book
        mock_project.published = False
        mock_project.import_project.return_value = mock_project

        # Chapter
        mock_chapter.number = 1
        mock_chapter.checked_level = 0
        mock_chapter.published = False
        mock_chapter.project = mock_project
        mock_chapter.comments = None
        mock_chapter.import_chapter.return_value = mock_chapter

        # Chunk
        mock_chunk.startv = 1
        mock_chunk.endv = 3
        mock_chunk.chapter = mock_chapter
        mock_chunk.comments = None
        mock_chunk.import_chunk.return_value = mock_chunk

        # Take
        mock_take.location = 'some path'
        mock_take.duration = 0
        mock_take.rating = 0
        mock_take.published = False
        mock_take.markers = ''
        mock_take.date_modified = '2018-07-02 1:53'
        mock_take.chunk = mock_chunk
        mock_take.comments = None
        mock_take.owner = None  #no user
        mock_take.import_take.return_value = mock_take

        # Comment
        mock_comment.location = "some path"
        mock_comment.date_modified = "2018-07-02 2:33"
        mock_comment.import_comment.return_value = True

        # TinyTag
        mock_tiny_tag.filehandler = None
        mock_tiny_tag.filsize = 0
        mock_tiny_tag.get.return_value = mock_tiny_tag

        # tasks.update_progress
        # mock_progress.return_value = True

        # FileUtility
        mock_file_utility.open_manifest_file.return_value = None
        mock_file_utility.manifest_takes_count.return_value = 2
        mock_file_utility.get_markers.return_value = 0

        # FileUtility.os.path
        mock_path.join.return_value = True
        mock_path.isfile.return_value = True

        # Set up data to pass into the import_project() function
        test_file_utility = FileUtility()
        test_directory = "some fake file path"
        test_user = {
            'user_icon_hash'  : 'fake hash',
            'user_name_audio' : 'fake_audio'
        }
        test_args = {
            'name'    : 'fake args',
            'message' : 'these are fake arguments'
        }

        print("Calculating actual value.\n")
        actual = test_file_utility.import_project(
            directory=test_directory,
            user=test_user,
            update_progress=mock_progress,
            task_args=test_args)
        print("Calculated actual value.\n")
        expected = {
            'user_icon_hash'  : 'fake hash',
            'user_name_audio' : 'fake_audio',
            'project_id'      :  1,
            'mode'            : 'chunk',
            'lang_slug'       : 'en',
            'lang_name'       : 'English',
            'book_slug'       : 'jos',
            'book_name'       : 'Joshua',
            'result'          : 'Imported 1 files of 1. '
        }
        self.assertEqual(expected, actual)
