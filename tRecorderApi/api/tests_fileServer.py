from django.test import TestCase
from datetime import datetime
from views import ProjectViewSet,FileUploadView, FileStreamView
from rest_framework.test import APIClient
from rest_framework import status
from pathlib import Path
import os


#Creating a text file to log the results of each of the tests
with open("test_log.txt", "w") as test_log:
    test_log.write("API TEST LOG\n")  #create title for test log
    sttime = datetime.now().strftime('%m/%d/%Y_%H:%M:%S') #create time stamp for test log
    test_log.write("DATE:" + sttime + "\n\n")  #print time stamp to test log
base_url = 'http://127.0.0.1:8000/api/'
my_file = 'C:/Users/ann_ejones/Documents/translationDB/tRecorderApi/media/dump'


#delete file from dump
#get file from dump,
#get JSON (?)
class fileServerTestCases(TestCase):
    def SetUp(self):
        """Set up environment for fileServer test suite"""
        self.client = APIClient()


    def test_fileServer_can_upload_file(self):
        """Verify that fileServer can upload file to dump folder through POST"""
        #list1 to search through dump folder
        list1 = os.listdir(my_file)
        old_count = len(list1)
        with open('en-x-demo2_ulb_mrk.zip', 'rb') as test_zip:
            response = self.client.post(base_url + 'upload/zip', {'Media type': '*/*', 'Content': test_zip}, format='multipart')
            #list2 to reinitialize the dump folder to count updates
            list2 = os.listdir(my_file)
            new_count = len(list2)
            self.assertNotEqual(old_count, new_count)
            test_log = open("test_log.txt", "a")
            test_log.write("TEST: File uploaded to file server.................................PASSED\n")
            test_log.close()


    def test_fileServer_can_get_file(self):
        """Verify that fileServer can retrieve file from dump folder through GET"""

        #get(self, request, filepath, format='mp3'):
        response = self.client.get(base_url + 'takes/1/')








