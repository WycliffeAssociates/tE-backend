from django.test import TestCase
from models import Take, Language, Book, User, Comment
from rest_framework.test import APIClient
from rest_framework import status
import os


base_url = 'http://127.0.0.1:8000/api/'
my_file = 'media/dump'
export_path = '/Users/nicholasdipinto1/Desktop/translationDB/8woc2017backend/tRecorderApi/en-x-demo2_ulb_mrk.zip'

#double check if creating test folder is practical - Not practical
#import views and test methods associated with views

#filepath = '/Users/lcheng/Desktop/8woc2017backend/tRecorderApi/media/dump/1499710960.9274436693-e236-4422-8a5c-72642ca4eaa7/en-x-demo2_ulb_b42_mrk_c07_v01_t05.wav'

class ViewTestCases(TestCase):
    def setUp(self):
        """Set up environment for api view test suite"""
        self.client = APIClient()
        self.take_data = {'location' : export_path, 'chapter' : 5, 'is_export' : True, 'is_source' : False}
        self.lang_data = {'lang' : 'english', 'code' : 'abc'}
        self.user_data = {'name' : 'tester', 'agreed' : True, 'picture' : 'test.pic'}
        self.comment = {'location':'test_location'}
        self.book_data = {'code':'ex', 'name' : 'english', 'booknum' : 5}
        self.take_object = Take(location= export_path, chapter=5, is_export=True, is_source=False, id=1, language_id=1, book_id=1, user_id=1)
        self.language_object = Language(slug='en-x-demo', name='english', id=1)
        self.book_object = Book(name='english', booknum=5, id=1)
        self.user_object = User(name='testy', agreed=True, picture='mypic.jpg', id=1)
        self.comment_object = Comment.objects.create(location='/test-location/', id=1)

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
        result = str(response.data) #convert data returned from post request to string so we can checkthe data inside
        self.assertEqual(response.status_code, status.HTTP_200_OK) #verifying that that we succesfully post to the API
        self.assertNotEqual(0, len(response.data)) #testing that api does not return nothing
        self.assertIn("'chapter': 5", result) #test that the term we searched for is in the data returned from the post request
        #freeing up the temporary database
        self.take_object.delete()
        self.user_object.delete()
        self.book_object.delete()

    def test_that_we_can_get_no_projects_from_api(self):
         """Testing that submitting a POST request to get projects JSON data that can be parsed into takes"""
         #saving objects in temporary database so they can be read by the API
         self.language_object.save()
         self.book_object.save()
         self.user_object.save()
         self.take_object.save()
         response = self.client.post(base_url + 'get_project/', {'chapter' : 6}, format='json') #telling the API that I want all takes that have chapter 6 of a book recorded, which there shoul be none of
         self.assertEqual(response.status_code, status.HTTP_200_OK) #verifying that that we succesfully post to the API
         self.assertEqual(0, len(response.data))
         self.assertEqual(response.data, [])
         #freeing up the temporary database
         self.take_object.delete()
         self.user_object.delete()
         self.book_object.delete()

    def test_is_the_zip_file_there(self):
        """Testing if there is a zip file in exports"""
        #saving objects in temporary database so they can be read by the API
        self.language_object.save()
        self.book_object.save()
        self.user_object.save()
        self.take_object.save()
        response = self.client.post(base_url + 'get_project/', {'chapter' : 5}, format='json')
        response = self.client.post(base_url + 'zipFiles/', {'chapter' : 5}, format='json') #telling the API that I want all takes that have chapter 5 of a book recorded
        #self.assertTrue(os.path.exists())
        self.assertEqual(response.status_code, status.HTTP_200_OK) #verifying that that we succesfully post to the API
        self.assertNotEqual(0, len(response.data)) #testing that api does not return nothing
        #freeing up the temporary database
        self.take_object.delete()
        self.user_object.delete()
        self.book_object.delete()

    def tearDown(self):
        os.system('rm -rf ' + my_file)  # cleaning out all files generated during tests
        os.system('mkdir ' + my_file)
