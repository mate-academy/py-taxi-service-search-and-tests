from django.test import TestCase

from taxi.models import Manufacturer, Car, Driver


class ModelsTest(TestCase):
    def setUp(self) -> None:
        self.driver = Driver.objects.create(
            username="testuser",
            first_name="Test",
            last_name="User",
            license_number="12345"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Test country"
        )

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} "
            f"{self.manufacturer.country}"
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} "
            f"{self.driver.last_name})"
        )

    def test_car_str(self):
        car = Car.objects.create(
            model="test",
            manufacturer=self.manufacturer,
        )
        car.drivers.add(self.driver)
        self.assertEqual(str(car), car.model)

    def test_driver_get_absolute_url(self):
        self.assertEqual(self.driver.get_absolute_url(), "/drivers/1/")
