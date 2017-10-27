from django.test import TestCase
from rest_framework.test import APIClient
from ..models import Project, Language, Book, Chapter, Chunk, Take, Anthology, Version, Mode
from django.conf import settings

view_url = 'http://127.0.0.1:8000/api/get_project_takes/'
base_url = 'http://127.0.0.1:8000/api/'
my_file = settings.BASE_DIR + 'media/dump'
location_wav = settings.BASE_DIR + '/en-x-demo2_ulb_b42_mrk_c06_v01-03_t11.wav'


class GetProjectsTestCases(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.lang = Language.objects.create(slug='en-x-demo', name='english')
        self.anthology = Anthology.objects.create(slug='ot', name="old testament")
        self.book = Book.objects.create(name='mark', number=5, slug='mrk', anthology= self.anthology)
        self.version = Version.objects.create(slug='ulb', name="Unlocked literal bible")
        self.mode = Mode.objects.create(slug="chk", name= "chunk", unit= 1)
        self.proj = Project.objects.create(version=self.version, mode=self.mode,
                                           anthology=self.anthology, language=self.lang,
                                           book=self.book)
        self.chap = Chapter.objects.create(number=1, checked_level=1, published=False, project=self.proj)
        self.chunk = Chunk.objects.create(startv=0, endv=3, chapter=self.chap)

        self.take = Take.objects.create(location=location_wav, published=True,
        duration=0, markers="{\"test\" : \"true\"}", rating=2, chunk=self.chunk
        )
        self.project_takes_data = {"language": "en-x-demo2", "version": "ulb", "book": "mrk", "chapter": 1}


    def test_get_projects(self):
        get_min_checked_level = Project.objects.filter().values_list()
        print(get_min_checked_level)

