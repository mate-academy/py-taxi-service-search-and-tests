from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car, Driver


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Honda",
            country="Japan"
        )

        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="maxitoska",
            password="max12345",
            first_name="Maxim",
            last_name="Danylchuk",
            license_number="ABM34567",
        )

    def test_driver_str(self):
        self.assertEqual(str(self.driver), "maxitoska (Maxim Danylchuk)")

    def test_get_absolute_url(self):
        driver = Driver.objects.get(id=1)
        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")

    def test_create_driver_with_license_number(self):
        username = "test_username"
        password = "test12345"
        license_number = "AVD22543"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )

        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        car = Car.objects.create(
            model="X5",
            manufacturer=manufacturer,

        )

        self.assertEqual(str(car), car.model)
