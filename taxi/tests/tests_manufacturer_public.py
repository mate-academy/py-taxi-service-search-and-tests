from django.test import TestCase, Client
from django.urls import reverse


class PublicManufacturerTests(TestCase):
    def setUp(self):
        self.client = Client()
        
    def test_public(self):
        res = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(res.status_code, 200)
