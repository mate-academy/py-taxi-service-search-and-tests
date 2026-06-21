from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Car, Manufacturer


class ModelsTest(TestCase):
    def setUp(self):
        self.manufacturer = (Manufacturer.objects.create
                             (name="Toyota", country="Japan"))

        self.car = (Car.objects.create
                    (model="Corolla", manufacturer=self.manufacturer))

        self.driver = get_user_model().objects.create_user(
            username="AlexKing",
            password="qwerty",
            first_name="Alex",
            last_name="Smith",
            license_number="KMZS12345",
        )

    def test_car_str(self):
        self.assertEqual(str(self.car), self.car.model)

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}",
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username}"
            f" ({self.driver.first_name} {self.driver.last_name})",
        )

    def test_create_driver_with_license(self):
        self.assertEqual(self.driver.license_number, "KMZS12345")
        self.assertTrue(self.driver.check_password("qwerty"))

    def test_create_car_and_driver(self):
        self.car.drivers.add(self.driver)
        self.assertIn(self.driver, self.car.drivers.all())
        self.assertIn(self.car, self.driver.cars.all())
