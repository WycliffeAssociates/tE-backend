from django.test import TestCase
from datetime import datetime
from views import ProjectViewSet,FileUploadView, FileStreamView
from rest_framework.test import APIClient
from rest_framework import status

#Creating a text file to log the results of each of the tests
with open("test_log.txt", "w") as test_log:
    test_log.write("API TEST LOG\n")  #create title for test log
    sttime = datetime.now().strftime('%m/%d/%Y_%H:%M:%S') #create time stamp for test log
    test_log.write("DATE:" + sttime + "\n\n")  #print time stamp to test log
base_url = 'http://127.0.0.1:8000/api/'

#create file in dump
#test to see it's there, assert it's there

#delete file from dump
#get file from dump,
#get JSON (?)
class fileServerTestCases(TestCase):
    def SetUp(self):
        """Set up environment for fileServer test suite"""
        self.client = APIClient()

    def test_fileServer_can_upload_file(self):
        """Verify that fileServer can upload file to dump folder"""
        with open('en-x-demo2_ulb_mrk.zip', 'rb') as test_zip:
            self.response = self.client.post(base_url + 'upload/zip', {'Media type': '*/*', 'Content': test_zip}, format='multipart')
            self.assertContains()



