import os
import shutil

from django.test import TestCase

from ..file_transfer.FileUtility import FileUtility
from ..file_transfer.Upload import Upload
from ..file_transfer.ZipIt import ZipIt
from ..models import Take


class UploadTestCases(TestCase):

    def test_create_root_directory(self):    #create a directory, verify if it exists and delete it
        fl = FileUtility()
        dir = fl.root_dir(['test', 'case'])
        dir_path = os.path.dirname(os.path.dirname(os.path.realpath(dir)))
        is_dir = os.path.isdir(dir)
        shutil.rmtree(dir_path)
        self.assertEqual(True, is_dir)

    def test_upload_zip_(self):       # TODO remove the file created
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_to_upload = os.path.join(dir_path, 'test_files/aaa_ulb_mat.zip')
        up = Upload(ZipIt(), None, FileUtility(), Take)
        resp, stat = up.upload(file_to_upload, 'zip')
        self.test_if_takes_saved_in_DB()
        self.assertEqual(resp, 'ok')
        self.assertEqual(stat, 200)

































