from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ManufacturerModelTest(TestCase):
    def test_manufacturer_str(self) -> None:
        manufacturer = Manufacturer(name="Tesla", country="USA")
        self.assertEqual(str(manufacturer), "Tesla USA")


class DriverModelTest(TestCase):
    def test_driver_str(self) -> None:
        driver = get_user_model().objects.create_user(
            username="john",
            password="john12345",
            first_name="John",
            last_name="Doe",
            license_number="JOD12345"
        )
        self.assertEqual(str(driver), "john (John Doe)")


class CarModelTest(TestCase):
    def test_car_str(self) -> None:
        manufacturer = Manufacturer(name="Tesla", country="USA")
        car = Car(model="Model S", manufacturer=manufacturer)
        self.assertEqual(str(car), "Model S")
