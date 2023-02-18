from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):

    def setUp(self) -> None:
        self.username = "test"
        self.password = "test1234"
        self.license_number = "QWE12345"
        self.driver = get_user_model().objects.create_user(
            username=self.username,
            password=self.password,
            first_name="test_first_name",
            last_name="test_last_name",
            license_number=self.license_number
        )
        self.manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )

    def test_manufacturer_str(self):
        self.assertEqual(str(self.manufacturer), f"{self.manufacturer.name} {self.manufacturer.country}")

    def test_driver_str(self):
        self.assertEqual(str(self.driver), f"{self.driver.username} ({self.driver.first_name} {self.driver.last_name})")

    def test_car_str(self):
        car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer,
        )

        self.assertEqual(str(car), f"{car.model}")

    def test_create_driver_with_license_number(self):
        self.assertEqual(self.driver.username, self.username)
        self.assertTrue(self.driver.check_password(self.password))
        self.assertEqual(self.driver.license_number, self.license_number)

    def test_driver_get_absolute_url(self):
        self.assertEqual(
            self.driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": self.driver.id})
        )
