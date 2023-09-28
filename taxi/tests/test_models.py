from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Driver, Car


class ManufacturerTestCase(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )
        self.driver = Driver.objects.create(
            username="testuser",
            first_name="John",
            last_name="Doe",
            license_number="123456"
        )
        self.car = Car.objects.create(
            model="Mustang",
            manufacturer=self.manufacturer
        )
        self.car.drivers.add(self.driver)

    def test_manufacturer_str_method(self):
        self.assertEqual(str(self.manufacturer), "Ford USA")

    def test_driver_str_method(self):
        self.assertEqual(str(self.driver), "testuser (John Doe)")

    def test_driver_absolute_url_method(self):
        expected_url = reverse(
            "taxi:driver-detail",
            kwargs={"pk": self.driver.pk}
        )
        self.assertEqual(self.driver.get_absolute_url(), expected_url)

    def test_car_str_method(self):
        self.assertEqual(str(self.car), "Mustang")
