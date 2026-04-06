from django.test import TestCase, Client
from django.urls import reverse

HOME_URL = reverse("taxi:index")


class PublicHomeTest(TestCase):
    def test_login_required(self):
        res = self.client.get(HOME_URL)
        self.assertNotEqual(res.status_code, 200)
