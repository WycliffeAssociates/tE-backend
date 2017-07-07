from django.test import TestCase
from datetime import datetime
from models import Take, Language, Book, User, Comment
from rest_framework.test import APIClient
from rest_framework import status

base_url = 'http://127.0.0.1:8000/api/'

class ViewTestCases(TestCase):
    def setUp(self):
        """Set up environment for api view test suite"""
        self.client = APIClient()
        self.take_data = {'location' : 'test_location', 'chapter' : 5}
        self.lang_data = {'lang' : 'english', 'code' : 'abc'}
        self.user_data = {'name' : 'tester', 'agreed' : True, 'picture' : 'test.pic'}
        self.comment = {'location':'test_location'}
        self.book_data = {'code':'ex', 'name' : 'english', 'booknum' : 5}
        self.take_object = Take(location='test_location', id=1, language_id=1, book_id=1, user_id=1)
        self.language_object = Language(slug='en-x-demo', name='english', id=1)
        self.book_object = Book(name='english', booknum=5, id=1)
        self.user_object = User(name='testy', agreed=True, picture='mypic.jpg', id=1)
        self.comment_object = Comment.objects.create(location='/test-location/', id=1)

############################## Testing POST Request #####################################################
    def test_api_can_create_take_object(self):
        """Test the API has take creation capability:
        Sending JSON Take Object To API and
        Expecting HTTP Success Message Returned"""
        self.response = self.client.post(base_url + 'takes/', self.take_data, format='json') #send POST to API
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_create_lang_object(self):
        """Test the API has lang creation capability:
        Sending JSON Lang Object To API and
        Expecting HTTP Success Message Returned"""
        self.response = self.client.post(base_url + 'languages/', self.lang_data,format='json')  # send POST to API
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_create_book_object(self):
        """Test the API has book creation capability:
        Sending JSON Book Object To API and
        Expecting HTTP Success Message Returned"""
        self.response = self.client.post(base_url + 'books/', self.book_data,format='json')  # send POST to API
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_create_comment_object(self):
        """Test the API has comment creation capability:
        Sending JSON Comment Object To API and
        Expecting HTTP Success Message Returned"""
        self.response = self.client.post(base_url + 'comments/', self.comment,format='json')  # send POST to API
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_that_api_can_create_user_object(self):
        """Test the API has user creation capability:
        Sending JSON User Object To API and
        Expecting HTTP Success Message Returned"""
        self.response = self.client.post(base_url + 'users/', self.user_data, format='json')
        self.assertEquals(self.response.status_code, status.HTTP_201_CREATED)
#######################################################################################################

############################### Testing Update Requests ###############################################

    def test_api_can_update_take_object(self):
        """Test that the API can update a take object:
        Sending Take Object To API and
        Expecting HTTP Success Message Returned"""
        self.take_object.save()
        response = self.client.put(base_url + 'takes/1/', {'location' : 'new_location'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.take_object.delete()
        self.assertEqual(0, len(Take.objects.filter(id=1)))

    def test_api_can_update_language_object(self):
        """Test that the API can update a language object:
        Sending Language Object To API and
        Expecting HTTP Success Message Returned"""
        self.language_object.save()
        response = self.client.put(base_url + 'languages/1/', {'code' : 'ex-demo'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.language_object.delete()
        self.assertEqual(0, len(Language.objects.filter(id=1)))

    def test_api_can_update_book_object(self):
        """Test that the API can update a book object:
        Sending Book Object To API and
        Expecting HTTP Success Message Returned"""
        self.book_object.save()
        response = self.client.put(base_url + 'books/1/', {'name': 'spanish'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book_object.delete()  # delete object from temporary database
        self.assertEqual(0, len(Book.objects.filter(id=1)))

    def test_api_can_update_user_object(self):
        """Test that the API can update a User object:
        Sending User Object To API and
        Expecting HTTP Success Message Returned"""
        self.user_object.save()
        response = self.client.put(base_url + 'users/1/', {'name' : 'nick', 'picture' : 'newpic.jpg'}, format='json') #picture is required to change when updating user object
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user_object.delete()  # delete object from temporary database
        self.assertEqual(0, len(User.objects.filter(id=1)))

    def test_api_can_update_comment_object(self):
        """Test that the API can update a User object:
        Sending User Object To API and
        Expecting HTTP Success Message Returned"""
        self.comment_object.save()
        response = self.client.put(base_url + 'comments/1/', {'location' : '/new-location/'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.comment_object.delete()  # delete object from temporary database
        self.assertEqual(0, len(Comment.objects.filter(id=1)))
#####################################################################################################

#################################### Testing GET Requests ###########################################

    def test_get_take_request_returns_success(self):
         """Testing API can handle GET requests for Take objects"""
         self.take_object.save()
         response = self.client.get(base_url + 'takes/1/')
         self.assertEqual(response.status_code, status.HTTP_200_OK)
         self.take_object.delete()    #delete object from temporary database
         self.assertEqual(0,len(Take.objects.filter(id=1)))  #check that take_object was deleted from temporary database

    def test_get_language_request_returns_success(self):
         """Testing API can handle GET requests for Language objects"""
         self.language_object.save()
         response = self.client.get(base_url + 'languages/1/')
         self.assertEqual(response.status_code, status.HTTP_200_OK)
         self.language_object.delete()    #delete object from temporary database
         self.assertEqual(0,len(Language.objects.filter(id=1)))  #check that object was deleted from temporary database

    def test_get_book_request_returns_success(self):
         """Testing API can handle GET requests for Book objects"""
         self.book_object.save()
         response = self.client.get(base_url + 'books/1/')
         self.assertEqual(response.status_code, status.HTTP_200_OK)
         self.book_object.delete()    #delete object from temporary database
         self.assertEqual(0,len(Book.objects.filter(id=1)))  #check that object was deleted from temporary database

    def test_get_user_request_returns_success(self):
         """Testing API can handle GET requests for User objects"""
         self.user_object.save()
         response = self.client.get(base_url + 'users/1/')
         self.assertEqual(response.status_code, status.HTTP_200_OK)
         self.user_object.delete()    #delete object from temporary database
         self.assertEqual(0,len(User.objects.filter(id=1)))  #check that object was deleted from temporary database

    def test_get_comment_request_returns_success(self):
         """Testing API can handle GET requests for Comment objects"""
         self.comment_object.save()
         response = self.client.get(base_url + 'comments/1/')
         self.assertEqual(response.status_code, status.HTTP_200_OK)
         self.comment_object.delete()    #delete object from temporary database
         self.assertEqual(0,len(Comment.objects.filter(id=1)))  #check that object was deleted from temporary database
#####################################################################################################

############################### Testing DELETE Requests #############################################

    def test_that_api_can_delete_take_objects(self):
        """Testing that the API has Take Object deletion functionality"""
        self.take_object.save()
        response = self.client.delete(base_url + 'takes/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK) #after deleting an object, nothing should be returned, which is why we check against a 204 status code
        self.take_object.delete()

    def test_that_api_can_delete_language_objects(self):
        """Testing that the API has Language Object deletion functionality"""
        self.language_object.save()
        response = self.client.delete(base_url + 'languages/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT) #after deleting an object, nothing should be returned, which is why we check against a 204 status code
        self.language_object.delete()

    def test_that_api_can_delete_book_objects(self):
        """Testing that the API has Take Object deletion functionality"""
        self.book_object.save()
        response = self.client.delete(base_url + 'books/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT) #after deleting an object, nothing should be returned, which is why we check against a 204 status code
        self.book_object.delete()

    def test_that_api_can_delete_user_objects(self):
        """Testing that the API has User Object deletion functionality"""
        self.user_object.save()
        response = self.client.delete(base_url + 'users/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT) #after deleting an object, nothing should be returned, which is why we check against a 204 status code
        self.user_object.delete()

    def test_that_api_can_delete_comment_objects(self):
        """Testing that the API has Take Object deletion functionality"""
        self.comment_object.save()
        response = self.client.delete(base_url + 'comments/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK) #after deleting an object, nothing should be returned, which is why we check against a 204 status code
        self.comment_object.delete()
#####################################################################################################

    def test_posting_file_to_api_returns_success_response(self):
        """Testing That zip files can be uploaded to the api"""
        with open('en-x-demo2_ulb_mrk.zip', 'rb') as test_zip:
         self.response = self.client.post(base_url + 'upload/zip', {'Media type' : '*/*', 'Content' : test_zip}, format='multipart')
         self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_that_we_can_get_projects(self):
        """Testing that submitting a POST request to get projects returns a JSON onbject"""
        #saving objects in temporary database so they can be read by the API
        self.language_object.save()
        self.book_object.save()
        self.user_object.save()
        self.take_object.save()
        response = self.client.post(base_url + 'get_project/', {'chapter' : 5}, format='json') #telling the API that I want all takes that have chapter 5 of a book recorded
        self.assertEqual(response.status_code, status.HTTP_200_OK) #verifying that that we succesfully post to the API
        #freeing up the temporary database
        self.take_object.delete()
        self.user_object.delete()
        self.book_object.delete()
