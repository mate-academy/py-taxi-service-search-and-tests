from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from taxi.models import Manufacturer

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class ManufacturerSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="user1234",
            license_number="ABC12345",
        )
        self.client.force_login(self.user)

        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

    def test_search_by_manufacturer_name(self):
        response = self.client.get(MANUFACTURER_LIST_URL, {"name": "Toyota"})
        manufacturer_list = response.context["manufacturer_list"]

        self.assertIn(self.manufacturer1, manufacturer_list)
        self.assertNotIn(self.manufacturer2, manufacturer_list)

    def test_search_manufacturer_name_is_case_insensitive(self):
        response = self.client.get(MANUFACTURER_LIST_URL, {"name": "toyota"})
        manufacturer_list = response.context["manufacturer_list"]

        self.assertIn(self.manufacturer1, manufacturer_list)

    def test_empty_manufacturer_search_returns_all(self):
        response = self.client.get(MANUFACTURER_LIST_URL, {"name": ""})
        manufacturer_list = response.context["manufacturer_list"]

        self.assertEqual(len(manufacturer_list), 2)
