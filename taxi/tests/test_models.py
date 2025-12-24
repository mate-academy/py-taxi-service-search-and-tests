from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        self.assertEqual(str(manufacturer),
                         f"{manufacturer.name} {manufacturer.country}")

    def test_driver_str(self):
        driver = Driver.objects.create_user(
            username="test",
            password="test1234",
            first_name="first",
            last_name="last",
        )
        self.assertEqual(str(driver),
                         f"{driver.username} ("
                         f"{driver.first_name} "
                         f"{driver.last_name})")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        car = Car.objects.create(model="test", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)

    def test_create_driver_with_correct_license(self):
        driver = Driver.objects.create_user(
            username="test",
            password="test1234",
            license_number="ASD12345",
        )

        self.assertEqual(driver.username, "test")
        self.assertTrue(driver.check_password("test1234"))
        self.assertTrue(driver.license_number, "ASD12345")

    def test_get_absolute_url(self):
        driver = Driver.objects.create_user(
            username="test",
            password="test1234",
            first_name="first",
            last_name="last",
        )
        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")
