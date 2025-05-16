from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test_name",
            country="Test_country"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test_name",
            country="Test_country"
        )
        driver = Driver.objects.create_user(
            license_number="Test_license_number",
            username="test_username",
            password="test123",
        )
        car = Car.objects.create(model="Test_model", manufacturer=manufacturer)
        car.drivers.set([driver])
        self.assertEqual(str(car), "Test_model")

    def test_driver_str(self):
        license_number = "Test_license_number"
        username = "test_username"
        password = "test123"
        first_name = "Test_first_name"
        last_name = "Test_last_name"
        driver = Driver.objects.create_user(
            license_number=license_number,
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_get_absolute_url(self):
        license_number = "Test_license_number"
        username = "test_username"
        password = "test123"
        first_name = "Test_first_name"
        last_name = "Test_last_name"
        driver = Driver.objects.create_user(
            license_number=license_number,
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        excepted_url = reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        self.assertEqual(driver.get_absolute_url(), excepted_url)
