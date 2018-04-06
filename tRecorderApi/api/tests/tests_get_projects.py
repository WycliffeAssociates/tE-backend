from django.test import TestCase
from django.conf import settings
from rest_framework.test import APIClient
# from django.forms.models import model_to_dict
from ..models import Project, Language, Book, Chapter, Chunk, Take, Anthology, Version, Mode
from ..serializers import ProjectSerializer

VIEW_URL = 'http://127.0.0.1:8000/api/get_project_takes/'
BASE_URL = 'http://127.0.0.1:8000/api/'
MY_FILE = settings.BASE_DIR + 'media/dump'
LOCATION_WAV = settings.BASE_DIR + '/en-x-demo2_ulb_b42_mrk_c06_v01-03_t11.wav'


class GetProjectsTestCases(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.lang = Language.objects.create(slug='en-x-demo',
                                            name='english')
        self.anthology = Anthology.objects.create(slug='ot',
                                                  name="old testament")
        self.book = Book.objects.create(name='mark',
                                        number=5,
                                        slug='mrk',
                                        anthology=self.anthology)
        self.version = Version.objects.create(slug='ulb',
                                              name="Unlocked literal bible")
        self.mode = Mode.objects.create(slug="chk",
                                        name="chunk",
                                        unit=1)
        self.proj = Project.objects.create(version=self.version,
                                           mode=self.mode,
                                           anthology=self.anthology,
                                           language=self.lang,
                                           book=self.book)
        self.proj.save()
        self.chap = Chapter.objects.create(number=1,
                                           checked_level=1,
                                           published=False,
                                           project=self.proj)
        self.chap2 = Chapter.objects.create(number=2,
                                            checked_level=2,
                                            published=False,
                                            project=self.proj)
        self.chap3 = Chapter.objects.create(number=3,
                                            checked_level=3,
                                            published=False,
                                            project=self.proj)
        self.chap4 = Chapter.objects.create(number=4,
                                            checked_level=0,
                                            published=False,
                                            project=self.proj)

        self.chunk = Chunk.objects.create(startv=0,
                                          endv=3,
                                          chapter=self.chap)
        self.chunk2 = Chunk.objects.create(startv=0,
                                           endv=3,
                                           chapter=self.chap2)
        self.chunk3 = Chunk.objects.create(startv=0,
                                           endv=3,
                                           chapter=self.chap3)
        self.chunk4 = Chunk.objects.create(startv=0,
                                           endv=3,
                                           chapter=self.chap4)
        self.chunk5 = Chunk.objects.create(startv=0,
                                           endv=3,
                                           chapter=self.chap4)
        self.chunk6 = Chunk.objects.create(startv=0,
                                           endv=3,
                                           chapter=self.chap4)

        self.take = Take.objects.create(location=LOCATION_WAV,
                                        published=True,
                                        duration=0,
                                        markers="{\"test\" : \"true\"}",
                                        rating=2,
                                        chunk=self.chunk)
        self.take = Take.objects.create(location=LOCATION_WAV,
                                        published=True,
                                        duration=0,
                                        markers="{\"test\" : \"true\"}",
                                        rating=2,
                                        chunk=self.chunk2)
        self.take = Take.objects.create(location=LOCATION_WAV,
                                        published=True,
                                        duration=0,
                                        markers="{\"test\" : \"true\"}",
                                        rating=2,
                                        chunk=self.chunk3)
        self.take = Take.objects.create(location=LOCATION_WAV,
                                        published=True,
                                        duration=0,
                                        markers="{\"test\" : \"true\"}",
                                        rating=2,
                                        chunk=self.chunk4)
        self.take.save()

        self.project_takes_data = {"language": "en-x-demo2",
                                   "version" : "ulb",
                                   "book"    : "mrk",
                                   "chapter" : 1
                                  }
        self.project_serializer = ProjectSerializer(instance=self.proj)

    def test_get_minimum_checked_level(self):
        min_check_level = Chapter.objects.all().values_list('checked_level') \
            .order_by('checked_level')[0][0]
        self.assertEqual(min_check_level, 0)

    def test_get_total_chunks(self):
        chunks_done = Chapter.objects.all().values_list('chunk').count()
        self.assertEqual(chunks_done, 6)

    def test_keys_in_project(self):
        """
        Verify that the ProjectSerializer class serializes an object of type
        'Project' into a JSON format containing the following assumed keys:
            1) id
            2)  published
            3)  contributors
            4)  date_modified
            5)  completed
            6)  checked_level
            7)  language
            8)  book
            9)  version
            10) anthology
        Input: data => serialized data of project object created in setup
        Expected: data will contain all of the keys listed above
        """

        data = self.project_serializer.data
        self.assertIn("id", data)
        self.assertIn("published", data)
        # self.assertIn("contributors", data)   project serializer does not
        # include this field
        self.assertIn("date_modified", data)
        self.assertIn("completed", data)
        # self.assertIn("checked_level", data) project field does not include
        # this field
        self.assertIn("language", data)
        self.assertIn("book", data)
        self.assertIn("version", data)
        self.assertIn("anthology", data)

    def test_get_percentage_function(self):
        chunks_done = 30
        total_chunks = 100
        percentage = Project.get_percentage_completed(chunks_done, total_chunks)
        self.assertEqual(percentage, 30)
