from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="Ford", country="USA")
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="lewis.hamilton",
            password="12password34",
            first_name="Lewis",
            last_name="Hamilton"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_book_str(self):
        manufacturer = Manufacturer.objects.create(name="Ford", country="USA")
        car = Car.objects.create(model="Mustang", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)

    def test_create_user_with_license_number(self):
        username = "lewis.hamilton"
        password = "12password34"
        license_number = "ABC12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
