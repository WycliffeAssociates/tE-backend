from django.test import TestCase
from rest_framework.test import APIClient
from ..models import Project
from django.conf import settings

view_url = 'http://127.0.0.1:8000/api/get_project_takes/'
base_url = 'http://127.0.0.1:8000/api/'
my_file = settings.BASE_DIR + 'media/dump'
location_wav = settings.BASE_DIR + '/en-x-demo2_ulb_b42_mrk_c06_v01-03_t11.wav'


class GetProjectsTestCases(TestCase):
    def setUp(self):
        self.client = APIClient()
        # self.lang = Language.objects.create(slug='en-x-demo', name='english')
        # self.book = Book.objects.create(name='mark', booknum=5, slug='mrk')
        #self.proj = Project.objects.create(version__slug='ulb', mode__name='chunk',
        #                                   anthology__slug='nt', is_source=False, language__slug='en',
        #                                   book__slug="mrk")
        # self.chap = Chapter.objects.create(number=1, checked_level=1, is_publish=False, project=self.proj)
        # self.chunk = Chunk.objects.create(startv=0, endv=3, chapter=self.chap)
        # self.user = User.objects.create(name='testy', agreed=True, picture='mypic.jpg')
        # self.take = Take.objects.create(location=location_wav, is_publish=True,
        # duration=0, markers="{\"test\" : \"true\"}", rating=2, chunk=self.chunk,
        # user=self.user)
        # self.project_takes_data = {"language": "en-x-demo2", "version": "ulb", "book": "mrk", "chapter": 1}

    # def test_that_we_can_get_projects(self):
    #     """Testing that submitting a POST request through key search returns a JSON object"""
    #
    #     self.response = self.client.post(view_url, self.project_takes_data,
    #                                      format='json')
    #     result = str(
    #         self.response.data)  # convert data returned from post request to string so we can checkthe data inside
    #     self.assertEqual(self.response.status_code,
    #                      status.HTTP_200_OK)  # verifying that that we succesfully post to the API
    #     self.assertIn("en-x-demo2",
    #                   result)  # test that the term we searched for is in the data returned from the post request
    #
    # def test_that_we_can_get_no_projects_from_api(self):
    #     """Testing that getting a project that does not exist from not enough parameters posted"""
    #     # saving objects in temporary database so they can be read by the API
    #
    #     self.response = self.client.post(view_url, {'location': my_file},
    #                                      format='json')
    #     # getting 400 error not enough parameters returned
    #     self.assertEqual(self.response.status_code,
    #                      status.HTTP_400_BAD_REQUEST)  # verifying that that we succesfully post to the API
    #
    # def tearDown(self):
    #     if platform == "darwin":  # OSX
    #         os.system('rm -rf ' + my_file)  # cleaning out all files generated during tests
    #         os.system('mkdir ' + my_file)
    #     elif platform == "win32":  # Windows
    #         os.system('rmdir /s /q ' + 'media\dump')  # cleaning out all files generated during tests
    #         os.system('mkdir ' + 'media\dump')
    #     self.take.delete()
    #     self.user.delete()
    #     self.chunk.delete()
    #     self.chap.delete()
    #     self.proj.delete()
    #     self.book.delete()
    #     self.lang.delete()

    def test_get_projects(self):
        get_min_checked_level = self.proj.objects.filter()
        print(get_min_checked_level)
        assert True
