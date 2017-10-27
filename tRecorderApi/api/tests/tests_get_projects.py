from django.test import TestCase
from rest_framework.test import APIClient
from ..models import Project, Language, Book, Chapter, Chunk, Take, Anthology, Version, Mode
from django.conf import settings
from django.forms.models import model_to_dict

view_url = 'http://127.0.0.1:8000/api/get_project_takes/'
base_url = 'http://127.0.0.1:8000/api/'
my_file = settings.BASE_DIR + 'media/dump'
location_wav = settings.BASE_DIR + '/en-x-demo2_ulb_b42_mrk_c06_v01-03_t11.wav'


class GetProjectsTestCases(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.lang = Language.objects.create(slug='en-x-demo', name='english')
        self.anthology = Anthology.objects.create(slug='ot', name="old testament")
        self.book = Book.objects.create(name='mark', number=5, slug='mrk', anthology=self.anthology)
        self.version = Version.objects.create(slug='ulb', name="Unlocked literal bible")
        self.mode = Mode.objects.create(slug="chk", name="chunk", unit=1)
        self.proj = Project.objects.create(version=self.version, mode=self.mode,
                                           anthology=self.anthology, language=self.lang,
                                           book=self.book)
        self.chap = Chapter.objects.create(number=1, checked_level=1, published=False, project=self.proj)
        self.chap2 = Chapter.objects.create(number=2, checked_level=2, published=False, project=self.proj)
        self.chap3 = Chapter.objects.create(number=3, checked_level=3, published=False, project=self.proj)
        self.chap4 = Chapter.objects.create(number=4, checked_level=0, published=False, project=self.proj)

        self.chunk = Chunk.objects.create(startv=0, endv=3, chapter=self.chap)
        self.chunk2 = Chunk.objects.create(startv=0, endv=3, chapter=self.chap2)
        self.chunk3 = Chunk.objects.create(startv=0, endv=3, chapter=self.chap3)
        self.chunk4 = Chunk.objects.create(startv=0, endv=3, chapter=self.chap4)
        self.chunk5 = Chunk.objects.create(startv=0, endv=3, chapter=self.chap4)
        self.chunk6 = Chunk.objects.create(startv=0, endv=3, chapter=self.chap4)

        self.take = Take.objects.create(location=location_wav, published=True,
                                        duration=0, markers="{\"test\" : \"true\"}", rating=2, chunk=self.chunk
                                        )
        self.take = Take.objects.create(location=location_wav, published=True,
                                        duration=0, markers="{\"test\" : \"true\"}", rating=2, chunk=self.chunk2
                                        )
        self.take = Take.objects.create(location=location_wav, published=True,
                                        duration=0, markers="{\"test\" : \"true\"}", rating=2, chunk=self.chunk3
                                        )
        self.take = Take.objects.create(location=location_wav, published=True,
                                        duration=0, markers="{\"test\" : \"true\"}", rating=2, chunk=self.chunk4
                                        )

        self.project_takes_data = {"language": "en-x-demo2", "version": "ulb", "book": "mrk", "chapter": 1}

    def test_get_minimum_checked_level(self):
        min_check_level = Chapter.objects.all().values_list('checked_level') \
            .order_by('checked_level')[0][0]
        self.assertEqual(min_check_level, 0)

    def test_get_total_chunks(self):
        chunks_done = Chapter.objects.all().values_list('chunk').count()
        self.assertEqual(chunks_done, 6)

    @staticmethod
    def test_build_dict():
        projects = Project.objects.all()
        project_list = []
        for project in projects:
            dic = {"id": project.id,
                   "published": project.published,
                   "contributors": [],
                   "version": {
                       "slug": project.version.slug,
                       "name": project.version.name
                   },
                   "anthology": {
                       "slug": project.anthology.slug,
                       "name": project.anthology.name
                   },
                   "language": {
                       "slug": project.language.slug,
                       "name": project.language.name
                   },
                   "book": {
                       "slug": project.book.slug,
                       "name": project.book.name,
                       "number": project.book.number
                   }
                   }
            latest_take = Take.objects.filter(chunk__chapter__project=project) \
                .latest("date_modified")

            dic["date_modified"] = latest_take.date_modified

            min_check_level = Chapter.objects.all().values_list('checked_level') \
                .order_by('checked_level')[0][0]

            chunks_done = Chapter.objects.all().values_list('chunk').count()
            takes = Take.objects.filter(chunk__chapter__project=project)

            dic["checked_level"] = min_check_level
            fake_total_chunks = 10
            completed = int(round((chunks_done / fake_total_chunks) * 100))
            dic["completed"] = completed

            project_list.append(dic)
