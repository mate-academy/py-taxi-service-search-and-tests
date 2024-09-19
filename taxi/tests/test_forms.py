from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="john.doe",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_search_manufacturers(self) -> None:
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="BMW", country="Germany")

        response = self.client.get(MANUFACTURER_URL, {"name": "toy"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "BMW")


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="john.doe",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_search_cars(self) -> None:
        toyota = Manufacturer.objects.create(name="Toyota", country="Japan")
        bmw = Manufacturer.objects.create(name="BMW", country="Germany")
        Car.objects.create(model="Yaris", manufacturer=toyota)
        Car.objects.create(model="X5 M", manufacturer=bmw)

        response = self.client.get(CAR_URL, {"model": "yar"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Yaris")
        self.assertNotContains(response, "X5 M")


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="john.doe",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_search_drivers(self) -> None:
        Driver.objects.create_user(
            username="admin.user",
            password="testPassword123",
            license_number="ADM56984"
        )

        response = self.client.get(DRIVER_URL, {"username": "john"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john.doe")
        self.assertNotContains(response, "admin.user")
