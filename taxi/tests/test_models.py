from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Test Kingdom"
        )

        self.assertEquals(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test123456",
            first_name="Test first",
            last_name="Test last"
        )

        self.assertEquals(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Test Kingdom"
        )
        car = Car.objects.create(
            model="Test model",
            manufacturer=manufacturer,
        )

        self.assertEquals(str(car), car.model)

    def test_create_driver_with_license_num(self):
        username = "test"
        password = "test123456"
        license_number = "LIS123456"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )

        self.assertEquals(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEquals(driver.license_number, license_number)

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test123456",
        )

        absolute_url = driver.get_absolute_url()

        self.assertEquals(absolute_url, f"/drivers/{driver.id}/")
