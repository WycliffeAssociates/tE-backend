from django.test import TestCase
from datetime import datetime
from models import Take, Language, Book, User, Comment
from rest_framework.test import APIClient
from rest_framework import status


#Creating a text file to log the results of each of the tests
with open("test_log.txt", "w") as test_log:
    test_log.write("API TEST LOG\n")  #create title for test log
    sttime = datetime.now().strftime('%m/%d/%Y_%H:%M:%S') #create time stamp for test log
    test_log.write("DATE:" + sttime + "\n\n")  #print time stamp to test log
base_url = 'http://127.0.0.1:8000/api/'

class ViewTestCases(TestCase):
    def setUp(self):
        """Set up environment for api view test suite"""
        self.client = APIClient()
        self.take_data = {'location' : 'test1.zip'}
        self.lang_data = {'lang' : 'english', 'code' : 'abc'}
        self.user_data = {'name' : 'tester', 'agreed' : True, 'picture' : 'test.pic'}
        self.comment = {'location':'test_location'}

    def test_api_can_create_take_object(self):
        """Test the API has take creation capability:
        Sending JSON File Object To API and
        Expecting HTTP Success Message Returned"""
        self.response = self.client.post(base_url + 'takes/', self.take_data, format='json') #send POST to API
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        test_log = open("test_log.txt", "a")
        test_log.write("TEST: Posting Take Object to API................................PASSED\n")
        test_log.close()

    def test_api_can_create_lang_object(self):
        """Test the API has lang creation capability:
        Sending JSON File Object To API and
        Expecting HTTP Success Message Returned"""
        self.response = self.client.post(base_url + 'languages/', self.lang_data,format='json')  # send POST to API
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        test_log = open("test_log.txt", "a")
        test_log.write("TEST: Posting Language Object to API............................PASSED\n")
        test_log.close()

    def test_api_can_create_comment_object(self):
        """Test the API has lang creation capability:
        Sending JSON File Object To API and
        Expecting HTTP Success Message Returned"""
        self.response = self.client.post(base_url + 'comments/', self.comment,format='json')  # send POST to API
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        test_log = open("test_log.txt", "a")
        test_log.write("TEST: Posting Comment Object to API.............................PASSED\n")
        test_log.close()

    def test_that_api_can_create_user_object(self):
        self.response = self.client.post(base_url + 'users/', self.user_data, format='json')
        self.assertEquals(self.response.status_code, status.HTTP_201_CREATED)
        test_log = open("test_log.txt", "a")
        test_log.write("TEST: Posting User Object to API................................PASSED\n")
        test_log.close()

    def test_api_can_update_take_object(self):
        """Test that the API can update a take object:
        Sending Take Object To API and
        Expecting HTTP Success Message Returned"""
        take_object = Take.objects.create(location='test_location', id=1)
        response = self.client.put(base_url + 'takes/1/', {'location' : 'new_location'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        take_object.delete()
        self.assertEqual(0, len(Take.objects.filter(id=1)))
        test_log = open("test_log.txt", "a")
        test_log.write("TEST: Sending PUT Request For Take Object To API................PASSED\n")
        test_log.close()

    def test_api_can_update_language_object(self):
        """Test that the API can update a language object:
        Sending Language Object To API and
        Expecting HTTP Success Message Returned"""
        language_object = Language.objects.create(code='en-demo',name='english', id=1)
        response = self.client.put(base_url + 'languages/1/', {'code' : 'ex-demo'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        language_object.delete()
        self.assertEqual(0, len(Language.objects.filter(id=1)))
        test_log = open("test_log.txt", "a")
        test_log.write("TEST: Sending PUT Request For Language Object To API............PASSED\n")
        test_log.close()

    def test_api_can_update_book_object(self):
        """Test that the API can update a book object:
        Sending Book Object To API and
        Expecting HTTP Success Message Returned"""
        book_object = Book.objects.create(code='en-demo', name='english', booknum=5, id=1)
        response = self.client.put(base_url + 'books/1/', {'name': 'spanish'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book_object.delete()  # delete object from temporary database
        self.assertEqual(0, len(Book.objects.filter(id=1)))
        test_log = open("test_log.txt", "a")
        test_log.write("TEST: Sending PUT Request For Book Object To API................PASSED\n")
        test_log.close()

    def test_api_can_update_user_object(self):
        """Test that the API can update a User object:
        Sending User Object To API and
        Expecting HTTP Success Message Returned"""
        user_object = User.objects.create(name='testy', agreed=True, picture='mypic.jpg', id=1)
        user_object.name = 'tester'
        response = self.client.put(base_url + 'users/1/', {'name' : 'nick', 'picture' : 'newpic.jpg'}, format='json') #picture is required to change when updating user object
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_object.delete()  # delete object from temporary database
        self.assertEqual(0, len(User.objects.filter(id=1)))
        test_log = open("test_log.txt", "a")
        test_log.write("TEST: Sending PUT Request For User Object To API................PASSED\n")
        test_log.close()

    def test_api_can_update_comment_object(self):
        """Test that the API can update a User object:
        Sending User Object To API and
        Expecting HTTP Success Message Returned"""
        comment_object = Comment.objects.create(location='/test-location/', id=1)
        response = self.client.put(base_url + 'comments/1/', {'location' : '/new-location/'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        comment_object.delete()  # delete object from temporary database
        self.assertEqual(0, len(Comment.objects.filter(id=1)))
        test_log = open("test_log.txt", "a")
        test_log.write("TEST: Sending PUT Request For Comment Object To API.............PASSED\n")
        test_log.close()

    def test_get_take_request_returns_success(self):
         """Testing API can handle GET requests for Take objects"""
         take_object = Take.objects.create(location='test_location', id=1)
         response = self.client.get(base_url + 'takes/1/')
         self.assertEqual(response.status_code, status.HTTP_200_OK)
         take_object.delete()    #delete object from temporary database
         self.assertEqual(0,len(Take.objects.filter(id=1)))  #check that take_object was deleted from temporary database
         test_log = open("test_log.txt", "a")
         test_log.write("TEST: Sending GET request for Take Object to API................PASSED\n")
         test_log.close()

    def test_get_language_request_returns_success(self):
         """Testing API can handle GET requests for Language objects"""
         language_object = Language.objects.create(code='en-demo',name='english', id=1)
         response = self.client.get(base_url + 'languages/1/')
         self.assertEqual(response.status_code, status.HTTP_200_OK)
         language_object.delete()    #delete object from temporary database
         self.assertEqual(0,len(Language.objects.filter(id=1)))  #check that object was deleted from temporary database
         test_log = open("test_log.txt", "a")
         test_log.write("TEST: Sending GET request for Language Object to API............PASSED\n")
         test_log.close()

    def test_get_book_request_returns_success(self):
         """Testing API can handle GET requests for Book objects"""
         book_object = Book.objects.create(code='en-demo',name='english', booknum=5, id=1)
         response = self.client.get(base_url + 'books/1/')
         self.assertEqual(response.status_code, status.HTTP_200_OK)
         book_object.delete()    #delete object from temporary database
         self.assertEqual(0,len(Book.objects.filter(id=1)))  #check that object was deleted from temporary database
         test_log = open("test_log.txt", "a")
         test_log.write("TEST: Sending GET request for Book Object to API................PASSED\n")
         test_log.close()

    def test_get_user_request_returns_success(self):
         """Testing API can handle GET requests for User objects"""
         user_object = User.objects.create(name='testy',agreed=True, picture='mypic.jpg', id=1)
         response = self.client.get(base_url + 'users/1/')
         self.assertEqual(response.status_code, status.HTTP_200_OK)
         user_object.delete()    #delete object from temporary database
         self.assertEqual(0,len(User.objects.filter(id=1)))  #check that object was deleted from temporary database
         test_log = open("test_log.txt", "a")
         test_log.write("TEST: Sending GET request for User Object to API................PASSED\n")
         test_log.close()

    def test_get_comment_request_returns_success(self):
         """Testing API can handle GET requests for Comment objects"""
         comment_object = Comment.objects.create(location='/test-location/', id=1)
         response = self.client.get(base_url + 'comments/1/')
         self.assertEqual(response.status_code, status.HTTP_200_OK)
         comment_object.delete()    #delete object from temporary database
         self.assertEqual(0,len(Comment.objects.filter(id=1)))  #check that object was deleted from temporary database
         test_log = open("test_log.txt", "a")
         test_log.write("TEST: Sending GET request for Comment Object to API.............PASSED\n")
         test_log.close()

    def test_posting_file_to_api_returns_success_response(self):
        """Testing That zip files can be uploaded to the api"""
        with open('en-x-demo2_ulb_mrk.zip', 'rb') as test_zip:
         self.response = self.client.post(base_url + 'upload/zip', {'Media type' : '*/*', 'Content' : test_zip}, format='multipart')
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