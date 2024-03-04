from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelTests(TestCase):
    def setUp(self) -> None:
        self.driver = Driver.objects.create_user(
            username="test_username",
            password="<PASSWORD>",
            license_number="test_license_number",
            first_name="test_first_name",
            last_name="test_last_name"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )

    def test_manufacturer_str(self):
        self.assertEqual(str(self.manufacturer), "test_name test_country")

    def test_driver_with_license_number(self):
        self.assertEqual(self.driver.username, "test_username")
        self.assertEqual(self.driver.license_number, "test_license_number")
        self.assertTrue(self.driver.check_password("<PASSWORD>"))

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            "test_username (test_first_name test_last_name)"
        )

    def test_car_str(self):
        car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer,
        )
        self.assertEqual(str(car), "test_model")
