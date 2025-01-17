from django.test import TestCase

from taxi.models import Driver, Car, Manufacturer


class ModelTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="test manufacturer",
            country="test country",
        )
        self.driver = Driver.objects.create(
            username="test",
            first_name="test_first_name",
            last_name="test_last_name",
            email="test@example.com",
            license_number="test_license_number",
        )

    def test_driver_str(self):
        self.assertEqual(str(self.driver),
                         f"{self.driver.username} "
                         f"({self.driver.first_name} "
                         f"{self.driver.last_name})")

    def test_car_str(self):
        car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer,
        )
        self.assertEqual(str(car), car.model)

    def test_create_driver_with_driver_license(self):
        self.assertEqual(self.driver.license_number, "test_license_number")
