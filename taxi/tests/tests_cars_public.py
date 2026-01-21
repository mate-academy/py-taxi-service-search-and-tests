from django.test import TestCase, Client
from django.urls import reverse


class PublicCarsTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_public(self):
        res = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(res.status_code, 200)
