from django.test import TestCase
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="testname", country="testcountry"
        )
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test",
            password="test123",
            license_number="YUU12345",
            first_name="firsttest",
            last_name="lasttest"
        )
        self.assertEqual(
            str(driver), f"{driver.username} "
                         f"({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="testname", country="testcountry"
        )
        car = Car.objects.create(model="testmodel", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)

    def test_create_driver_with_license(self):
        username = "testusername"
        password = "test123"
        license_number = "TTT12345"

        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.create(
            username="test",
            password="test123",
            license_number="YUU12345",
            first_name="firsttest",
            last_name="lasttest"
        )
        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")
