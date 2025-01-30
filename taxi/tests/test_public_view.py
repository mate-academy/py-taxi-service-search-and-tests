from django.test import TestCase
from django.urls import reverse


class PublicPageTest(TestCase):
    def test_login_required(self):
        res = self.client.get(reverse("taxi:index"))
        self.assertNotEqual(res.status_code, 200)
