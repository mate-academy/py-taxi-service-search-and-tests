from django.test import TestCase, Client
from django.urls import reverse


class PublicDriversTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_public(self):
        res = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(res.status_code, 200)
