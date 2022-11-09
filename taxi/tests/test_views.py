from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.test import TestCase

from django.urls import reverse

from taxi.forms import SearchForm
from taxi.models import Manufacturer


class TestAccessViews(TestCase):
    def test_login_required(self):
        urls = [
            reverse("taxi:driver-list"),
            reverse("taxi:car-list"),
            reverse("taxi:manufacturer-list"),
            reverse("taxi:index")
        ]
        for url in urls:
            with self.subTest(url=url):
                resp = self.client.get(url)
                self.assertNotEqual(resp.status_code, 200)
