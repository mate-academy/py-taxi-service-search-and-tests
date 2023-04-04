from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test1",
            country="Test2"
        )
        self.assertEqual(str(manufacturer),
                         f"{manufacturer.name} {manufacturer.country}")

    def test_drivers_first_name_label(self):
        get_user_model().objects.create_user(
            username="test",
            password="1234test123",
            first_name="Pimp",
            last_name="Lazo"
        )
        field_label = Driver._meta.get_field("first_name").verbose_name
        self.assertEqual(field_label, "first name")

    def test_get_absolute_url(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="1234test123",
            first_name="Pimp",
            last_name="Lazo"
        )
        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test1",
            country="Test2"
        )
        car = Car.objects.create(
            model="TestModel",
            manufacturer=manufacturer
        )

        self.assertEqual(str(car), car.model)

    def test_create_driver_with_license(self):
        username = "test"
        password = "test1234"
        license_number = "ABC12345"

        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )

        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
