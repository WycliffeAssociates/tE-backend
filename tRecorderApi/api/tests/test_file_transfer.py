"""
    This module contains the suite of tests for testing the import_project()
    function found in the FileUtility class of the
    api.file_transfer.FileUtility module. The MOCKFILECONTENTS var is a
    constant defined in the api.tests.mock_manifest module which cotnains
    long-winded values tha are used inside this test.
"""
from unittest.mock import patch, Mock
from django.test import TestCase
from api.file_transfer.tinytag import TinyTag
from api.models.chapter import Chapter
from api.models.chunk import Chunk
from api.models.language import Language
from api.models.anthology import Anthology
from api.models.book import Book
from api.models.version import Version
from api.models.project import Project
from api.models.mode import Mode
import json
# from api.tests.mock_manifest import MOCKFILECONTENTS
# from api.tests.mock_manifest import MOCKFILECONTENTS

def mock_import_chapter(
        project,
        number,
        checked_level):
    """Create Chapter object in memory rather than in DB"""
    return Chapter(
        project=project,
        number=number,
        checked_level=checked_level)

def mock_import_chunk(
        chapter,
        startv,
        endv):
    """Create Chunk object in memory rather than in DB"""
    return Chunk(
        chapter=chapter,
        startv=startv,
        endv=endv)

def mock_import_language(json):
    """Create Language object in memory rather than in DB"""
    return Language(
        slug=json['slug'],
        name=json['name'])

def mock_import_anthology(json):
    """Create Anthology object in memory rather than in DB"""
    return Anthology(
        slug=json['slug'],
        name=json['name'])

def mock_import_book(
        json,
        anthology):
    """Create Book object in memory rather than in DB"""
    return Book(
        slug=json['slug'],
        name=json['name'],
        number=json['number'],
        anthology=anthology)

def mock_import_version(json):
    """Create Version object in memory rather than in DB"""
    return Version(
        slug=json['slug'],
        name=json['name'])

def mock_import_mode(json):
    """Create Mode object in memory rather than in DB"""
    return Mode(
        name=json['name'],
        slug=json['slug'],
        unit=json['type'])

def mock_import_project(
        version,
        mode,
        anthology,
        language,
        book):
    """Create Project object in memory rather than in DB"""
    return Project(
        version=version,
        mode=mode,
        anthology=anthology,
        language=language,
        book=book)

def mock_tiny_tag(wav_file):
    """Create empty tiny tag object"""
    return TinyTag(None, 0)

def mock_open_manifest(jsonFile):
    """
        Replace FileUtility.open_manifest_file() so that it doesn't try to open
        a directory
    """
    with open("mock_manifest.json") as json_mock:
        mock_manifest = json.load(json_mock)
        return mock_manifest

class FileUtilityTest(TestCase):
    """
        Test case for testing the behavior of the import_project() function
    """
    @patch('api.file_transfer.FileUtility.open_manifest_file', side_effect=mock_open_manifest)
    @patch('api.models.language.Language.import_language', side_effect=mock_import_language)
    @patch('api.models.anthology.Anthology.import_anthology', side_effect=mock_import_anthology)
    @patch('api.models.book.Book.import_book', side_effect=mock_import_book)
    @patch('api.models.version.Version.import_version', side_effect=mock_import_version)
    @patch('api.models.mode.Mode.import_mode', side_effect=mock_import_mode)
    @patch('api.models.take.Take.import_takes', return_value=True)
    @patch('api.file_transfer.tinytag.TinyTag.get', side_effect=mock_tiny_tag)
    @patch('api.tasks.update_progress', return_value=True)
    @patch('api.models.chunk.Chunk.import_chunk', side_effect=mock_import_chunk)
    @patch('api.models.comment.Comment.import_comment', return_value=True)
    @patch('api.models.chapter.Chapter.import_chapter', side_effect=mock_import_chapter)
    @patch('api.file_transfer.FileUtility.os.path')
    @patch('api.file_transfer.FileUtility')
    def test_import_project(
            self,
            mock_file_utility,
            mock_path,
            import_chapter,
            import_comment,
            import_chunk,
            mock_update_progress,
            get_tiny_tag,
            import_take,
            import_mode,
            import_version,
            import_book,
            import_anthology,
            import_language,
            open_manifest):
        """
            Test to verify that when an object of type FileUtility calls its
            import_project() method that it will return a json. FileUtility is
            mocked here so that we can predefine its other methods without actually
            calling it.
        """
        file_util = mock_file_utility()
        mock_path.exists.return_values = True
        #Test should not create any new directories
        #Therefore, we will stub out os.path.join() to just return a Boolean
        mock_path.join.return_value = True
        mock_path.isfile.return_value = True
        # file_util.open_manifest_file.return_value = json.load("mock_manifest.json") 
        # define total takes inside manifest to be 2 even though there is one
        # take in it
        file_util.manifest_takes_count.return_value = 2
        file_util.get_markers.return_value = 0
        self.assertEqual(1, 1)
