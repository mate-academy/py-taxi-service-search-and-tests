from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        self.driver_password = "test123"
        self.driver_username = "test_usermane"
        self.driver_first_name = "test_first_name"
        self.driver_last_name = "test_last_name"
        self.driver_license_number = "test_license"
        self.driver = get_user_model().objects.create_user(
            password=self.driver_password,
            username=self.driver_username,
            first_name=self.driver_first_name,
            last_name=self.driver_last_name,
            license_number=self.driver_license_number
        )
        self.car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer
        )

    def test_manufacturer_str(self) -> None:
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )

    def test_driver_str(self) -> None:
        self.assertEqual(
            str(self.driver),
            (
                f"{self.driver.username} "
                f"({self.driver.first_name} "
                f"{self.driver.last_name})"
            )
        )

    def test_driver_get_absolute_url(self) -> None:
        self.assertEqual(
            self.driver.get_absolute_url(),
            reverse(
                "taxi:driver-detail", kwargs={"pk": self.driver.pk}
            )
        )

    def test_driver_check_fields(self) -> None:
        self.assertEqual(self.driver.first_name, self.driver_first_name)
        self.assertEqual(self.driver.last_name, self.driver_last_name)
        self.assertEqual(self.driver.username, self.driver_username)
        self.assertEqual(
            self.driver.license_number,
            self.driver_license_number
        )
        self.assertTrue(self.driver.check_password(self.driver_password))

    def test_car_str(self) -> None:
        self.assertEqual(str(self.car), self.car.model)
