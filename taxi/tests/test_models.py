from django.test import TestCase
from django.urls import reverse

from taxi.tests.helpers import create_test_data


class ModelsTests(TestCase):
    def setUp(self):
        self.manufacturer, self.driver, self.car = create_test_data()

    def test_manufacturer_str(self):
        manufacturer = self.manufacturer
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = self.driver
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        car = self.car
        self.assertEqual(str(car), car.model)

    def test_driver_get_absolute_url(self):
        driver = self.driver
        expected_url = reverse(
            "taxi:driver-detail",
            kwargs={"pk": driver.id}
        )
        self.assertEqual(
            driver.get_absolute_url(),
            expected_url
        )
