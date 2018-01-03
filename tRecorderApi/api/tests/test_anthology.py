from django.http import HttpResponsePermanentRedirect
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Anthology


class AnthologyTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        Anthology.objects.create(name='New Testament', slug='nt')
        Anthology.objects.create(name='Old Testament', slug='ot')

    def test_number_of_items_are_equal(self):
        anthology_num = Anthology.objects.count()
        response = self.client.get('/api/anthologies/')
        self.assertEqual(len(response.data), anthology_num)

    def test_get_request_has_200_status_code(self):
        response = self.client.get('/api/anthologies/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_request_with_id_has_200_status_code(self):
        response = self.client.get('/api/anthologies/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_request_with_id_has_200_status_code(self):
        response = self.client.get('/api/anthologies/?id=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_request_with_non_existent_id_has_404_status_code(self):
        response = self.client.get('/api/anthologies/4/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_random_text_as_parameter_gives_400_status_code(self):
        response = self.client.get('/api/anthologies/?randomeparameter/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
