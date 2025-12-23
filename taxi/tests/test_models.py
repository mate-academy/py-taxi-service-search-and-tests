from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class ModelsTestCase(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Suzuki",
            country="Japan"
        )
        self.driver = Driver.objects.create_user(
            username="john_doe",
            first_name="John",
            last_name="Doe",
            password="testpassword",
            license_number="12345"
        )
        self.car = Car.objects.create(
            model="Suzuki Vitara",
            manufacturer=self.manufacturer
        )
        self.car.drivers.add(self.driver)

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            "Suzuki Japan"
        )

    def test_driver_get_absolute_url(self):
        url = self.driver.get_absolute_url()
        self.assertEqual(url, reverse(
            "taxi:driver-detail",
            kwargs={"pk": self.driver.pk})
        )

    def test_driver_license_number(self):
        self.assertEqual(self.driver.license_number, "12345")

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} "
            f"{self.driver.last_name})"
        )

    def test_car_str(self):
        self.assertEqual(str(self.car), "Suzuki Vitara")

    def test_car_drivers(self):
        self.assertIn(self.driver, self.car.drivers.all())
