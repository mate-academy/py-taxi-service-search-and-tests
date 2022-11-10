from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicManufacturerTest(TestCase):
    def test_login_required_for_manufacturers(self):
        result = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(result.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(
            name="test name",
            country="test country"
        )
        result = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(result.status_code, 200)
        self.assertEqual(
            list(result.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(result, "taxi/manufacturer_list.html")


class PublicCarList(TestCase):
    def test_login_required_for_cars(self):
        result = self.client.get(CAR_URL)

        self.assertNotEqual(result.status_code, 200)


class PublishDriverList(TestCase):
    def test_login_required_for_drivers(self):
        result = self.client.get(DRIVER_URL)

        self.assertNotEqual(result.status_code, 200)
