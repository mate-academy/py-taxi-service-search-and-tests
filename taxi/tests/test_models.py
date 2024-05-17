from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Car, Manufacturer, Driver


class ModelsTest(TestCase):
    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test_username",
            first_name="test_name",
            last_name="test_surname"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_create_driver_with_license_number(self):
        username = "test_username",
        license_number = "test_license_number"
        driver = get_user_model().objects.create(
            username=username,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )
        car = Car.objects.create(model="test_model", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)

    def test_get_absolute_url(self):
        driver = Driver.objects.create(
            username="test_user",
            first_name="Test",
            last_name="User",
            license_number="ABC123"
        )
        expected_url = reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        self.assertEqual(driver.get_absolute_url(), expected_url)
