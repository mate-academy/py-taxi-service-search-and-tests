from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="Tesla", country="USA")
        self.assertEqual(str(manufacturer), "Tesla USA")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="mecho",
            password="Secretpw1",
            first_name="Mister",
            last_name="Echo"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_create_driver_license_number(self):
        username = "mecho"
        pw = "Secretpw1"
        license_number = "Hello123"

        driver = get_user_model().objects.create_user(
            username=username,
            password=pw,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(pw))

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="Tesla", country="USA")
        driver = get_user_model().objects.create(
            username="mecho",
            password="Secretpw1",
            first_name="Mister",
            last_name="Echo"
        )
        car = Car.objects.create(model="Model X",
                                 manufacturer=manufacturer,
                                 )
        car.drivers.set([driver])

        self.assertEqual(str(car), f"{car.model}")
