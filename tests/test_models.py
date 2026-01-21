from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class ModelTests(TestCase):
    def test_manufacturer_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Manufacturer",
            country="Country",
        )

        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}")

    def test_car_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Manufacturer",
            country="Country",
        )

        car = Car.objects.create(
            model="model",
            manufacturer=manufacturer,
        )

        self.assertEqual(str(car), car.model)

    def test_driver_str(self) -> None:
        driver = get_user_model().objects.create(
            username="User",
            first_name="Firstname",
            last_name="Lastname"
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_create_driver_with_license_number(self) -> None:
        username = "user"
        license_number = "QWE12345"

        driver = get_user_model().objects.create(
            username=username,
            license_number=license_number
        )

        self.assertEqual(username, driver.username)
        self.assertEqual(license_number, driver.license_number)

    def test_get_absolute_url(self) -> None:
        driver = Driver.objects.create(
            username="User",
            first_name="Firstname",
            last_name="Lastname",
            license_number="QWE12345"
        )

        expected_url = reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        self.assertEqual(driver.get_absolute_url(), expected_url)
