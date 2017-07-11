from django.test import TestCase
from models import Take, Language, User, Comment, Book

#Creating a text file to log the results of each of the tests
class ModelTestCase(TestCase):
    """This class defines the test suite for the each of the models."""

#    def test_model_can_create_a_take(self):
#        """Test the File model can create a take."""
#        old_count = Take.objects.count()  #obtain current count of object in database
#        self.take.save()   #save object to database
#        new_count = Take.objects.count()  #obtain new count of object in database
#        self.assertNotEqual(old_count, new_count)
#        test_log = open("test_log.txt", "a")  #append test results to test log
#        test_log.write("TEST: Creating and Storing a Take Object........................PASSED\n")
#        test_log.close()#

    def test_model_can_create_a_take(self):
        """Test the File model can create a take."""
        old_count = Take.objects.count()  #obtain current count of object in database
        self.take.save()   #save object to database
        new_count = Take.objects.count()  #obtain new count of object in database
        self.assertNotEqual(old_count, new_count)

    def test_model_can_create_a_Language(self):
        """Test the Language model can create a language."""
        old_count = Language.objects.count()
        self.language.save()
        new_count = Language.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_model_can_create_a_User(self):
        """Test the User model can create a user."""
        old_count = User.objects.count()
        self.user.save()
        new_count = User.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_model_can_create_a_Comment(self):
        """Test the Comment model can create a comment."""
        old_count = Comment.objects.count()
        self.comment.save()
        new_count = Comment.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_model_can_create_a_Book(self):
        """Test the Language model can create a language."""
        old_count = Book.objects.count()
        self.book.save()
        new_count = Book.objects.count()
        self.assertNotEqual(old_count, new_count)