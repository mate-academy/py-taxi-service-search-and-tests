from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test", country="test1"
        )
        manufacturer_expected = f"{manufacturer.name} {manufacturer.country}"
        self.assertEqual(str(manufacturer), manufacturer_expected)

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test12345",
            first_name="Test first",
            last_name="Test last"
        )

        driver_expected = f"{driver.username} " \
                          f"({driver.first_name} " \
                          f"{driver.last_name})"

        self.assertEqual(str(driver), driver_expected)

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test", country="test1"
        )
        car = Car.objects.create(model="test", manufacturer=manufacturer)

        car_expected = f"{car.model}"

        self.assertEqual(str(car), car_expected)

    def test_create_driver_licence_number(self):
        username = "test"
        password = "test12345"
        license_number = "license_number"

        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )

        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
