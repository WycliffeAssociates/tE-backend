from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Version


class VersionApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.version = Version.objects.create(slug='ulb', name="Unlocked literal bible")

    def test_number_of_items_are_equal(self):
        language_num = Version.objects.count()
        response = self.client.get('/api/versions/')
        self.assertEqual(len(response.data), language_num)

    def test_get_request_has_200_status_code(self):
        response = self.client.get('/api/versions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_request_with_id_has_200_status_code(self):
        response = self.client.get('/api/versions/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_request_with_id_has_200_status_code(self):
        response = self.client.get('/api/versions/?id=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_request_with_non_existent_id_has_404_status_code(self):
        response = self.client.get('/api/versions/4/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_random_text_as_parameter_gives_400_status_code(self):
        # 400 was expected status code but 200 is returned

        response = self.client.get('/api/versions/?randomeparameter/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_slug_equals_en_x_demo_as_parameter_has_len_one(self):
        response = self.client.get('/api/versions/?slug=ulb')
        self.assertEqual(len(response.data), 1)
