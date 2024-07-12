from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Car, Manufacturer


class ModelsTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create(
            username="test",
            password="test123",
            first_name="test_first",
            last_name="test_last",
            license_number="ABC12345",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Test Name",
            country="Test Country",
        )

    def test_driver_str(self):
        expected_driver_object_name = (f"{self.driver.username} "
                                       f"({self.driver.first_name} "
                                       f"{self.driver.last_name})")
        self.assertEqual(expected_driver_object_name, str(self.driver))

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.get(id=1)
        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")

    def test_manufacturer_str(self):
        expected_manufacturer_object_name = (f"{self.manufacturer.name} "
                                             f"{self.manufacturer.country}")
        self.assertEqual(
            expected_manufacturer_object_name,
            str(self.manufacturer)
        )

    def test_car_str(self):
        car = Car.objects.create(
            model="Test Model",
            manufacturer_id=1,
        )
        expected_car_object_name = f"{car.model}"
        self.assertEqual(expected_car_object_name, str(car))
