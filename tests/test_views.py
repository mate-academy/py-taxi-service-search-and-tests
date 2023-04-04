from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")


class PublicManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(response.status_code, 200)


class PublicCarTests(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_URL)

        self.assertNotEqual(response.status_code, 200)


class PublicDriverTests(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(
            name="Test",
            country="TestCountry"
        )
        Manufacturer.objects.create(
            name="Test2",
            country="TestCountry2"
        )

        response = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_manufacturer_with_search(self):
        response = self.client.get(MANUFACTURER_URL + "?name=B")

        manufacturers = Manufacturer.objects.filter(name__icontains="B")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
