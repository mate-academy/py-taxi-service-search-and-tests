from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class TestManufacturer(TestCase):
    def setUp(self):
        self.name = "Test Manufacturer"
        self.country = "Test Country"
        self.manufacturer = Manufacturer.objects.create(
            name=self.name,
            country=self.country,
        )

    def test_manufacturer_str(self):
        self.assertEqual(str(self.manufacturer), f"{self.name} {self.country}")


class TestDriver(TestCase):
    def setUp(self):
        self.username = "Test User"
        self.password = "password"
        self.first_name = "First"
        self.last_name = "Last"
        self.user = get_user_model().objects.create_user(
            username=self.username,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.user),
            f"{self.username} ({self.first_name} {self.last_name})"
        )

    def test_driver_get_absolute_url(self):
        url = reverse("taxi:driver-detail", kwargs={"pk": self.user.pk})
        self.assertEqual(url, self.user.get_absolute_url())


class TestCar(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country",
        )
        self.model = "Test Car"
        self.car = Car.objects.create(
            model=self.model,
            manufacturer=self.manufacturer,
        )

    def test_car_str(self):
        self.assertEqual(str(self.car), f"{self.model}")
