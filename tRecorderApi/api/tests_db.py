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
class ModelTestCase(TestCase):
    """This class defines the test suite for the each of the models."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.file_location = "uploads/file.zip"
        self.take = Take(location=self.file_location)
        self.language = Language(code='abc', name='english')
        self.user = User(name='tester', agreed=True, picture='test.pic')
        self.comment = Comment(location='test_location')

    def test_model_can_create_a_take(self):
        """Test the File model can create a file."""
        old_count = Take.objects.count()  #obtain current count of object in database
        self.take.save()   #save object to database
        new_count = Take.objects.count()  #obtain new count of object in database
        self.assertNotEqual(old_count, new_count)
        test_log = open("test_log.txt", "a")  #append test results to test log
        test_log.write("TEST: Creating and Storing a Take Object........................PASSED\n")
        test_log.close()

    def test_model_can_create_a_Project(self):
        """Test the Project model can create a file."""
        old_count = Language.objects.count()
        self.language.save()
        new_count = Language.objects.count()
        self.assertNotEqual(old_count, new_count)
        test_log = open("test_log.txt", "a")
        test_log.write("TEST: Creating and Storing a Project Object.....................PASSED\n")
        test_log.close()

    def test_model_can_create_a_User(self):
        """Test the User model can create a file."""
        old_count = User.objects.count()

        self.user.save()
        new_count = User.objects.count()
        self.assertNotEqual(old_count, new_count)
        test_log = open("test_log.txt", "a")
        test_log.write("TEST: Creating and Storing a User Object........................PASSED\n")
        test_log.close()

    def test_model_can_create_a_Comment(self):
        """Test the Comment model can create a file."""
        old_count = Comment.objects.count()
        self.comment.save()
        new_count = Comment.objects.count()
        self.assertNotEqual(old_count, new_count)
        test_log = open("test_log.txt", "a")
        test_log.write("TEST: Creating and Storing a Comment Object.....................PASSED\n")
        test_log.close()

    def test_each_model_can_be_read_in_a_human_readable_format(self):
        """Each Model has a __unicode__() which prints a readable name to the DB
        This test makes sure each model's unicode method outputs correctly"""
        self.assertEqual('None-', self.take.__unicode__())
        self.assertEqual("english", self.language.__unicode__())
        self.assertEqual("tester", self.user.__unicode__())
        #self.assertEqual("english-ub-mrk", self.meta.__unicode__())
        self.assertEqual("test_location", self.comment.__unicode__())
        test_log = open("test_log.txt", "a")
        test_log.write("TEST: Printing Each Model's Unicode.............................PASSED\n")
        test_log.close()