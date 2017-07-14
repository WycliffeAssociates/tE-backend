from django.test import TestCase
from views import md5Hash

class HelperTestCases(TestCase):

    def unit_testing_md5Hash_method_for_equality_with_duplicate_wav_files(self):
        # create object later when this is added to views.py
        # helpers.md5Hash('chapter.wav')
        # helpers.md5Hash('chapter.wav')
        self.assertEqual(md5Hash('chapter.wav'), md5Hash('chapter.wav'))


    def unit_testing_md5Hash_method_for_inequality_with_different_wav_files(
        self):  # create object later when this is in views.py
            hash1 = md5Hash('language.json')
            hash2 = md5Hash('en-x-demo2_ulb_b42_mrk_c07_v33-35_t04.wav')
            self.assertEqual(hash1, hash2)
            # helpers.md5Hash('language.json')