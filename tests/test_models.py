from django.test import TestCase
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="ZAZ", country="Ukraine"
        )
        self.driver = get_user_model().objects.create_user(
            username="super.mario",
            password="!@#456Qw",
            first_name="Mario",
            last_name="Super",
            license_number="ABC12345"
        )

    def test_manufacturer_str(self):
        manufacturer = self.manufacturer
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} "
            f"{manufacturer.country}"
        )

    def test_driver_str_and_license_number(self):
        driver = self.driver
        self.assertEqual(
            str(driver),
            f"{driver.username} "
            f"({driver.first_name} "
            f"{driver.last_name})"
        )
        self.assertEqual(
            driver.license_number,
            "ABC12345"
        )

    def test_driver_get_absolute_url(self):
        driver = self.driver
        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")

    def test_car_str(self):
        car = Car.objects.create(
            model="Test2",
            manufacturer=self.manufacturer
        )
        self.assertEqual(str(car.model), car.model)
