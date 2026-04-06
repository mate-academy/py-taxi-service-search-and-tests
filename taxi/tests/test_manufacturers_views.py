from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class ManufacturerSearchTestTest(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(
            username="admin",
            password="test123",
        )
        self.client.login(username="admin", password="test123")

        Manufacturer.objects.create(
            name="Ford",
            country="Falcon",
        )
        Manufacturer.objects.create(
            name="Honda",
            country="Japan",
        )
        Manufacturer.objects.create(
            name="Toyota GGO",
            country="USA",
        )
        Manufacturer.objects.create(
            name="Volvo",
            country="British Columbia",
        )

    def test_search_by_model(self):
        response = self.client.get(
            MANUFACTURER_URL,
            {"name": "Honda"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Honda")
        self.assertNotContains(response, "Toyota GGO")
        self.assertNotContains(response, "Volvo")
        self.assertNotContains(response, "Ford")

    def test_search_case_insensitive(self):
        response = self.client.get(
            MANUFACTURER_URL,
            {"name": "toYota ggO"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota GGO")
        self.assertNotContains(response, "Ford")
        self.assertNotContains(response, "Honda")
        self.assertNotContains(response, "Volvo")

    def test_empty_search_returns_all(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": ""}
        )
        self.assertContains(response, "Toyota GGO")
        self.assertContains(response, "Ford")
        self.assertContains(response, "Honda")
        self.assertContains(response, "Volvo")
