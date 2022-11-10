from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ManufacturerTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name", country="test_country"
        )

        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )


class DriverTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test_username",
            password="test_password",
            first_name="test_first_name",
            last_name="test_last_name",
            license_number="ASD12345",
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver), "test_username (test_first_name test_last_name)"
        )

    def test_driver_password_work_correct(self):
        self.assertTrue(self.driver.check_password("test_password"))

    def test_license_number_work_correct(self):
        self.assertEquals(self.driver.license_number, "ASD12345")


class CarTest(TestCase):
    def test_car_str(self):
        car = Car.objects.create(
            model="test_model",
            manufacturer=Manufacturer.objects.create(
                name="test_name", country="test_country"
            ),
        )
        self.assertEqual(str(car), "test_model")
