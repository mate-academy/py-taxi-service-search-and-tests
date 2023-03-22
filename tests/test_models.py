from django.test import TestCase
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test", country="Lviv"
        )
        self.driver = get_user_model().objects.create_user(
            username="Test",
            password="12121212@A",
            first_name="Test",
            last_name="User",
            license_number="ABC12345"
        )

    def test_manufacturer_str(self):
        manufacturer = self.manufacturer
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} "
            f"{manufacturer.country}"
        )

    def test_driver_str(self):
        driver = self.driver
        self.assertEqual(
            str(driver),
            f"{driver.username} "
            f"({driver.first_name} "
            f"{driver.last_name})"
        )

    def test_car_str(self):
        car = Car.objects.create(
            model="BMW F20",
            manufacturer=self.manufacturer
        )
        self.assertEqual(str(car.model), car.model)
