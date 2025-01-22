from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Driver, Manufacturer


class ModelTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="driver",
            password="driver123",
            first_name="test_first",
            last_name="test_last",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username}"
            f" ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        car = Car.objects.create(model="Corolla", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)

    def test_creat_driver_with_license_number(self):
        username = "driver"
        password = "driver123"
        license_number = "test123456"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))

    def test_driver_absolute_url(self):
        driver = get_user_model().objects.create_user(
            username="driver",
            password="driver123",
            first_name="test_first",
            last_name="test_last",
        )
        expected_url = reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        self.assertEqual(driver.get_absolute_url(), expected_url)
