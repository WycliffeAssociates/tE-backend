from django.test import TestCase
from models import Take, Language, User, Comment, Book
# Creating a text file to log the results of each of the tests

class ModelTestCase(TestCase):
    """This class defines the test suite for the each of the models."""

    def setUp(self):
        self.book_data = {'code': 'ex', 'name': 'english', 'booknum': 5}
        self.take = Take(location='test_location', chapter=5, is_export=True, is_source=False, id=1, language_id=1,
                         book_id=1, user_id=1)
        self.language = Language(slug='en-x-demo', name='english', id=1)
        self.book = Book(name='english', booknum=5, id=1)
        self.user = User(name='testy', agreed=True, picture='mypic.jpg', id=1)
        self.comment = Comment(location='/test-location/', id=1)


    def test_model_can_create_a_take(self):
        """Test the File model can create a take."""
        old_count = Take.objects.count()  # obtain current count of object in database
        self.take.save()  # save object to database
        new_count = Take.objects.count()  # obtain new count of object in database
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
        """Test the Book model can create a book."""
        old_count = Book.objects.count()
        self.book.save()
        new_count = Book.objects.count()
        self.assertNotEqual(old_count, new_count)

