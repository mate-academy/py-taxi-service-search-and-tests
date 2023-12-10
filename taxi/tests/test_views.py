from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Car, Driver, Manufacturer

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")
CAR_LIST_URL = reverse("taxi:car-list")


class PublicManufacturerTest(TestCase):
    def test_login_requirement(self):
        resp = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(resp.status_code, 200)


class PublicDriverTest(TestCase):
    def test_login_requirement(self):
        resp = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(resp.status_code, 200)


class PublicCarTest(TestCase):
    def test_login_requirement(self):
        resp = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(resp.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_login_requirement(self):
        resp = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(resp.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_login_requirement(self):
        resp = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(resp.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_login_requirement(self):
        resp = self.client.get(CAR_LIST_URL)
        self.assertEqual(resp.status_code, 200)
