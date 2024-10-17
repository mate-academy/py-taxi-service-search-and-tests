from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="TestName", country="TestCountry"
        )
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_create_author_with_license_number(self) -> None:
        username = "TestUsername"
        password = "TestPassword"
        license_number = "ABC12345"

        driver = get_user_model().objects.create_user(
            username=username, password=password, license_number=license_number
        )

        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))

    def test_driver_str(self) -> None:
        username = "TestUsername"
        first_name = "TestFirstName"
        last_name = "TestLastName"

        driver = Driver.objects.create(
            username=username, first_name=first_name, last_name=last_name
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_absolute_url(self) -> None:
        driver = get_user_model().objects.create_user(
            username="TestUser",
            password="TestPassword",
            license_number="ABC12345"
        )
        expected_url = reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        self.assertEqual(driver.get_absolute_url(), expected_url)

    def test_car_str(self) -> None:
        model = "X5 M"
        manufacturer = Manufacturer.objects.create(
            name="TestName", country="TestCountry"
        )

        driver = get_user_model().objects.create_user(
            username="TestUser",
            password="TestPassword",
            license_number="ABC12345"
        )

        car = Car.objects.create(
            model=model,
            manufacturer=manufacturer,
        )

        car.drivers.add(driver)

        self.assertEqual(str(car), car.model)
