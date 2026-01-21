from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTest(TestCase):
    def test_manufacturer_format_str(self):
        format_ = Manufacturer.objects.create(name="Test", country="Testland")
        self.assertEqual(str(format_), f"{format_.name} {format_.country}")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="Test2",
            password="Test2345",
            first_name="Uni",
            last_name="Test",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Testland"
        )
        car = Car.objects.create(model="Real Test", manufacturer=manufacturer)

        self.assertEqual(str(car), "Real Test")

    def test_driver_license_number(self):
        username = "Test2"
        password = "Test2345"
        license_number = "AAA12345"

        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )

        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
