from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import DriverLicenseUpdateForm
from taxi.models import Manufacturer, Car, Driver


class ModelTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Test"
        )

        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        user = get_user_model().objects.create_user(
            username="test",
            password="pass12345678",
            first_name="Test first",
            last_name="Test last"
        )

        self.assertEqual(str(user), (
            f"{user.username} ({user.first_name} {user.last_name})"
        ))

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Test"
        )

        car = Car.objects.create(
            model="Test",
            manufacturer=manufacturer,

        )

        self.assertEqual(str(car), car.model)

    def test_create_driver_with_license_number(self):
        username = "test"
        license_number = "ABC12345"

        driver = get_user_model().objects.create_user(
            username=username,
            license_number=license_number
        )

        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)

    def test_license_number_is_valid(self):
        license_number = DriverLicenseUpdateForm(
            data={"license_number": "ABC12345"}
        )

        self.assertTrue(license_number.is_valid())

    def test_license_number_is_not_be_longer_than_8(self):
        license_number = DriverLicenseUpdateForm(
            data={"license_number": "ABC1234523"}
        )

        self.assertFalse(license_number.is_valid())

    def test_license_number_should_has_3_uppercase(self):
        license_number = DriverLicenseUpdateForm(
            data={"license_number": "ACHD1234523"}
        )

        self.assertFalse(license_number.is_valid())

    def test_license_number_should_has_5_numbers(self):
        license_number = DriverLicenseUpdateForm(
            data={"license_number": "ACD1234523"}
        )

        self.assertFalse(license_number.is_valid())

    def test_get_absolute_url_in_driver(self):
        driver = get_user_model().objects.create_user(
            username="Test",
            password="test1234"
        )
        self.assertEquals(driver.get_absolute_url(), "/drivers/1/")
