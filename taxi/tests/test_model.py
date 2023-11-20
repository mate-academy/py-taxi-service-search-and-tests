from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="Porsche", country="Germany")
        self.assertEqual(str(manufacturer), f"{manufacturer.name} {manufacturer.country}")

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="capsparrow",
            password="test123456",
            first_name="Jack",
            last_name="Sparrow"
        )
        self.assertEqual(str(driver),
                         f"{driver.username} ({driver.first_name} {driver.last_name})")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="Toyota")
        car = Car.objects.create(
            model="Toyota Land Cruiser",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), car.model)

    def test_create_driver_with_license_number(self):
        license_number = "XAF54321"
        driver = get_user_model().objects.create(
            username="capsparrow",
            password="test123456",
            first_name="Jack",
            last_name="Sparrow",
            license_number=license_number
        )
        self.assertEqual(driver.license_number, license_number)



