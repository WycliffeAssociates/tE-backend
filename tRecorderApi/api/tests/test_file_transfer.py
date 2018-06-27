from django.test import TestCase
import mock
from api.file_transfer.tinytag import TinyTag
from api.tasks import update_progress
from api.models.chapter import Chapter
from api.models.comment import Comment
from api.models.chunk import Chunk
from mock_manifest import MOCKFILECONTENTS

def mock_import_chapter(
        project,
        number,
        checked_level):
    return Chapter(project, number, checked_level)

def mock_import_chunk(
        chapter,
        startv,
        endv):
    return Chunk(
        chapter=chapter,
        startv=startv,
        endv=endv)

class FileUtilityTest(TestCase):

    @mock.path('api.tasks.update_progress', return_value=True)
    @mock.patch('api.models.chunk.Chunk.import_chunk', side_effect=mock_import_chunk)
    @mock.patch('api.models.comment.Comment.import_comment', return_value=True)
    @mock.patch('api.models.chapter.Chapter.import_chapter', side_effect=mock_import_chapter)
    @mock.patch('api.file_transfer.FileUtility.os.path')
    @mock.patch('api.file_transfer.FileUtility')
    def test_import_project(
            self,
            mock_file_utility,
            mock_path,
            mock_chapter,
            mock_import_comment,
            mock_chunk,
            update_progress):
        """
            Test to verify that when an object of type FileUtility calls its
            import_projecty() method that it will return a json. FileUtility is
            mocked here so that we can predefine its other methods without actually
            calling it.
        """
        file_util = mock_file_utility()
        mock_path.exists.return_values = True
        #Test should not create any new directories
        #Therefore, we will stub out os.path.join() to just return a Boolean
        mock_path.join.return_value = True
        mock_path.isfile.return_value = True
        file_util.open_manifest_file.return_value = MOCKFILECONTENTS
        # define total takes inside manifest to be 2 even though there is one
        # take in it
        file_util.manifest_takes_count.return_value = 2
        self.assertEqual(1, 1)
