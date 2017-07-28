from django.test import TestCase
from api.models import Take, Language, Book, User, Comment, Chunk, Chapter, Project
from rest_framework.test import APIClient
from rest_framework import status
from django.conf import settings

view_url = 'http://127.0.0.1:8000/api/all_projects/'
my_file = settings.BASE_DIR + '/en-x-demo2_ulb_b42_mrk_c06_v01-03_t11.wav'


class AllProjectViewTestCases(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.lang = Language.objects.create(slug='en-x-demo', name='english')
        self.book = Book.objects.create(name='mark', booknum=5, slug='mrk')
        self.proj = Project.objects.create(version='ulb', mode='chunk',
                                           anthology='nt', is_source=False, language=self.lang,
                                           book=self.book)
        self.chap = Chapter.objects.create(number=1, checked_level=1, is_publish=False, project=self.proj)
        self.chunk = Chunk.objects.create(startv=0, endv=3, chapter=self.chap)
        self.user = User.objects.create(name='testy', agreed=True, picture='mypic.jpg')
        self.take = Take.objects.create(location=my_file, is_publish=True,
                                        duration=0, markers="{\"test\" : \"true\"}", rating=2, chunk=self.chunk,
                                        user=self.user)
        self.project_data = {"version": "ulb", "mode": "chunk", "anthology": "nt"}


    def test_post_request_for_all_projects_view(self):
        """Testing that sending a POST request to the All Project View returns a list of projects"""
        self.response = self.client.post(view_url,{"language":"en-x-demo2"}, format='json')
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        #check that response contains data
        self.assertNotEqual(0,len(str(self.response)))

    def tearDown(self):
        self.take.delete()
        self.user.delete()
        self.chunk.delete()
        self.chap.delete()
        self.proj.delete()
        self.book.delete()
        self.lang.delete()