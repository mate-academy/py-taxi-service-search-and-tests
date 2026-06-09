from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from taxi.models import Driver, Manufacturer, Car


class ModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.username = "DriverUsername"
        cls.license_number = "ADM12345"
        cls.model_name = "CarModel"

        cls.driver = Driver.objects.create_user(
            username=cls.username,
            password="DriverPassword",
            first_name="DriverFirstName",
            last_name="DriverLastName",
            license_number=cls.license_number,
        )

        cls.manufacturer = Manufacturer.objects.create(
            name="ManufacturerName",
            country="ManufacturerCountry",
        )

        cls.car = Car.objects.create(
            model=cls.model_name,
            manufacturer=cls.manufacturer,
        )

        cls.car.drivers.add(cls.driver)

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            "DriverUsername (DriverFirstName DriverLastName)"
        )

    def test_driver_get_absolute_url(self):
        self.assertEqual(self.driver.get_absolute_url(), "/drivers/1/")

    def test_driver_license_number_valid(self):
        self.assertEqual(self.driver.license_number, self.license_number)

    def test_invalid_license_raises_error(self):
        with self.assertRaises(ValidationError):
            driver = Driver(
                username="test1234",
                password="password1234",
                license_number="ADM12345"
            )
            driver.full_clean()

    def test_duplicate_license_number_does_not_save(self):
        with self.assertRaises(IntegrityError):
            Driver.objects.create_user(
                username="test1234",
                password="test1234",
                license_number="ADM12345"
            )

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            "ManufacturerName ManufacturerCountry"
        )

    def test_car_str(self):
        self.assertEqual(str(self.car), self.model_name)
