from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.models import Manufacturer, Car, Driver


class ModelsTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="test")
        self.assertEqual(manufacturer.name, "test")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test12345",
            first_name="test1",
            last_name="test2"
        )
        self.assertEqual(str(driver),
                         f"{driver.username} ({driver.first_name} "
                         f"{driver.last_name})")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="Tesla", country="USA")
        car = Car.objects.create(model="lamba", manufacturer=manufacturer)
        self.assertEqual(str(car), "lamba")

    def test_driver_license_number(self):
        driver = get_user_model().objects.create_user(
            username="test",
            license_number="WRT12345"
        )
        self.assertEqual(driver.license_number, "WRT12345")
        self.assertEqual(driver.username, "test")
