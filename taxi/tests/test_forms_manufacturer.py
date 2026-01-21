from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer


MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class ManufacturerSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Toyota", country="Japan")

    def test_manufacturer_search_without_query(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "BMW")
        self.assertContains(res, "Toyota")

    def test_manufacturer_search_with_correct_query(self):
        res = self.client.get(MANUFACTURER_URL, {"name": "toy"})
        self.assertEqual(res.status_code, 200)
        self.assertNotContains(res, "BMW")
        self.assertContains(res, "Toyota")

    def test_manufacturer_search_with_wrong_query(self):
        res = self.client.get(MANUFACTURER_URL, {"name": "YYY"})
        self.assertEqual(res.status_code, 200)
        self.assertNotContains(res, "BMW")
        self.assertNotContains(res, "Toyota")
