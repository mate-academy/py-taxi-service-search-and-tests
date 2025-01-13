from django.test import TestCase, Client
from django.urls import reverse

URL = reverse("taxi:manufacturer-list")


class PublicManufacturerFormatTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(URL)
        self.assertNotEqual(res.status_code, 200)
