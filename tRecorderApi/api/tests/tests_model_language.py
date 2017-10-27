from django.test import TestCase
from api.models import Language

class LanguageModelTests(TestCase):
    
    def test_gets_languages():
        language=Language.get_language()
        