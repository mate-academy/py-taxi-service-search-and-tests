from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerViewsTests(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerViewsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="driver",
            email="<EMAIL>",
            password="<PASSWORD>",
            license_number="ABC12345",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(
            name="Land Rover",
            country="United Kingdom",
        )
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)

        manufacturer = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer)
        )
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_list.html"
        )

    def test_manufacturer_search(self):
        Manufacturer.objects.create(
            name="Land Rover",
            country="United Kingdom",
        )
        Manufacturer.objects.create(
            name="Mercedes-Benz",
            country="Germany",
        )
        manufacturer = Manufacturer.objects.filter(name="Land Rover")
        response = self.client.get(f"{MANUFACTURER_URL}?name=land")
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer)
        )
