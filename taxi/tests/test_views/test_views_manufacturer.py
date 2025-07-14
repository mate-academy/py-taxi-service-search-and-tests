from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(
            name="BMV",
            country="Germany",
        )
        Manufacturer.objects.create(
            name="FIAT",
            country="Italy",
        )
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        search_response = self.client.get(f"{MANUFACTURER_URL}?name=BM")
        self.assertContains(search_response, "BMV")
        self.assertNotContains(search_response, "FIAT")

    def test_manufacturers_pagination(self):
        for num in range(6):
            Manufacturer.objects.create(
                name=f"TestManufacturer{num}",
                country=f"TestCountry{num}",
            )
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(len(response.context["manufacturer_list"]), 5)
