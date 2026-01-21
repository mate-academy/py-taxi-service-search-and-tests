from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Driver, Manufacturer, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="United States"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} "
            f"{manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test_driver",
            password="test1234",
            first_name="test_first",
            last_name="test_last",
            license_number="ABC12345"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} "
            f"({driver.first_name} "
            f"{driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="United States"
        )
        driver = get_user_model().objects.create(
            username="test_driver",
            password="test1234",
            first_name="test_first",
            last_name="test_last",
            license_number="ABC12345"
        )
        car = Car.objects.create(model="Audi", manufacturer=manufacturer)
        car.drivers.add(driver)
        self.assertEqual(str(car), car.model)

    def test_create_driver_with_license_number(self):
        username = "test_driver"
        password = "test1234"
        license_number = "ABC12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.license_number, license_number)
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.create_user(
            username="test_driver",
            password="test1234",
            first_name="test_first",
            last_name="test_last",
            license_number="ABC12345"
        )
        self.assertEqual(driver.get_absolute_url(), f"/drivers/{driver.id}/")
