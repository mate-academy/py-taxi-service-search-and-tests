from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.models import Driver, Car, Manufacturer


class ModelsTest(TestCase):
    def _create_manufacturer(self):
        return Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )

    def test_manufacturer_str(self):
        manufacturer = self._create_manufacturer()
        self.assertEqual(
            str(manufacturer),
            "Test Manufacturer Test Country"
        )

    def test_car_str(self):
        manufacturer = self._create_manufacturer()
        car = Car.objects.create(
            model="Test Car",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), "Test Car")

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="Test Driver",
            password="Test Password",
            first_name="Test First Name",
            last_name="Test Last Name"
        )
        self.assertEqual(
            str(driver),
            "Test Driver (Test First Name Test Last Name)"
        )

    def test_create_driver_with_license(self):
        username = "Test Driver"
        password = "Test Password"
        license_number = "ABC12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
