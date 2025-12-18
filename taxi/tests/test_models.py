from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="TestManufacturer",
            country="US"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="username",
            first_name="first_name",
            last_name="last_name",
            password="password",
            license_number="license_number",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_create_driver_with_license_number(self):
        license_number = "test"
        driver = get_user_model().objects.create(
            username="username",
            password="password",
            license_number=license_number,
        )
        self.assertEqual(driver.license_number, license_number)

    def test_driver_absolute_url(self):
        driver = get_user_model().objects.create(
            username="username",
            password="password",
            license_number="license_number",
        )
        expected_url = reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        self.assertEqual(driver.get_absolute_url(), expected_url)

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="TestManufacturer")
        driver = get_user_model().objects.create_user(
            username="driver1",
            password="testpass123"
        )

        car = Car.objects.create(
            model="model",
            manufacturer=manufacturer,
        )
        car.drivers.add(driver)
        self.assertEqual(str(car), car.model)
