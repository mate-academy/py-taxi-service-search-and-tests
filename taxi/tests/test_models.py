from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class ModelTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.assertEqual(str(manufacturer), "BMW Germany")

    def test_driver_str(self):
        driver = Driver.objects.create(
            username="test",
            first_name="first_name",
            last_name="last_name",
            license_number="QWE12345"
        )
        self.assertEqual(str(driver), "test (first_name last_name)")

    def test_get_absolute_url_driver(self):
        driver = Driver.objects.create(
            username="test",
            first_name="first_name",
            last_name="last_name",
            license_number="QWE12345"
        )
        expected_url = reverse(
            "taxi:driver-detail",
            kwargs={"pk": driver.pk}
        )
        self.assertEqual(driver.get_absolute_url(), expected_url)

    def test_car_str(self):
        car = Car.objects.create(
            model="BMW",
            manufacturer=Manufacturer.objects.create(
                name="BMW",
                country="Germany"
            ),
        )
        self.assertEqual(str(car), "BMW")
