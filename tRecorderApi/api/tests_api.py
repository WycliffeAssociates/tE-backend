from django.test import TestCase
from django.core.files import File
from .models import Take, Language, User, Comment
from datetime import datetime
from rest_framework.test import APIClient
from rest_framework import status


#Creating a text file to log the results of each of the tests
with open("test_log.txt", "w") as test_log:
    test_log.write("API TEST LOG\n")  #create title for test log
    sttime = datetime.now().strftime('%m/%d/%Y_%H:%M:%S') #create time stamp for test log
    test_log.write("DATE:" + sttime + "\n\n")  #print time stamp to test log

class ViewTestCases(TestCase):
    def setUp(self):
        """Set up environment for api view test suite"""
        self.client = APIClient()
        self.take_data = {'location' : 'test1.zip'}
        self.lang_data = {'lang' : 'english', 'code' : 'abc'}
        #self.user_data = {'name' : 'tester', 'agreed' : True, 'picture' : 'test.pic'}
        self.comment = {'location':'test_location'}

    def test_api_can_create_file_object(self):
        """Test the API has file creation capability:
        Sending JSON File Object To API and
        Expecting HTTP Success Message Returned"""
        self.response = self.client.post('http://127.0.0.1:8000/api/files/', self.take_data, format='json') #send POST to API
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        test_log = open("test_log.txt", "a")
        test_log.write("TEST: Posting Take Object to API................................PASSED\n")
        test_log.close()

    def test_api_can_create_lang_object(self):
        """Test the API has lang creation capability:
        Sending JSON File Object To API and
        Expecting HTTP Success Message Returned"""
        self.response = self.client.post('http://127.0.0.1:8000/api/languages/', self.lang_data,format='json')  # send POST to API
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        test_log = open("test_log.txt", "a")
        test_log.write("TEST: Posting Language Object to API............................PASSED\n")
        test_log.close()

    def test_api_can_create_comment_object(self):
        """Test the API has lang creation capability:
        Sending JSON File Object To API and
        Expecting HTTP Success Message Returned"""
        self.response = self.client.post('http://127.0.0.1:8000/api/comments/', self.comment,format='json')  # send POST to API
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        test_log = open("test_log.txt", "a")
        test_log.write("TEST: Posting Comment Object to API.............................PASSED\n")
        test_log.close()

    # def test_api_can_update_file_object(self):
    #       """Test the API has file creation capability:
    #       Sending JSON File Object To API and
    #       Expecting HTTP Success Message Returned"""
    #       change_file = {'location' : 'new_file'}
    #       response = self.client.put('http://127.0.0.1:8000/api/files/' + str(change_file.id), change_file, format='json')
    #       self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_posting_file_to_api_returns_success_response(self):
        """Testing That zip files can be uploaded to the api"""
        with open('test.zip', 'rb') as test_zip:
         self.response = self.client.post('http://127.0.0.1:8000/api/upload/zip', {'Media type' : '*/*', 'Content' : test_zip}, format='multipart')
         self.assertEqual(self.response.status_code, status.HTTP_200_OK)
         test_log = open("test_log.txt", "a")
         test_log.write("TEST: Uploading ZIP File to API.................................PASSED\n")
         test_log.close()

    # def test_client_can_post_project_to_api(self):
    #     self.response = self.client.post('http://127.0.0.1:8000/api/get_project', {'language' : 'english', 'slug' : 'ulb', 'chapter' : 1}, format='json')
    #     self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    # def test_that_api_does_not_accept_uploads_other_files(self):
    #     """Testing that uploading something that is not a file will return a HTTP 404 code"""
    #     self.response = self.client.post('http://127.0.0.1:8000/api/upload/zip', self.file_data, format='multipart')
    #     self.assertEqual(self.response.status_code, status.HTTP_404_NOT_FOUND)

    #def test_api_can_update_####_object:
        ######
        #####

    #def test_api_can_delete_####_object:
        ######
        #####