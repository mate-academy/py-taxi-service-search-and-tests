from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer(name="Volvo", country="Sweden")
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_car_str(self):
        manufacturer = Manufacturer(name="Volvo", country="Sweden")
        car = Car(
            model="LDS NFS",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), car.model)

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test1234",
            first_name="Miwa",
            last_name="TESTtest"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_license(self):
        driver = get_user_model().objects.create_user(
            username="miwa_test",
            password="supersecret",
            license_number="MMM12554"
        )
        self.assertTrue(driver.check_password("supersecret"))
        self.assertEqual(driver.license_number, "MMM12554")