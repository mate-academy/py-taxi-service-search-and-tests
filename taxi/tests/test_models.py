from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class TestModels(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country",
        )
        self.driver = Driver.objects.create(
            username="test_driver",
            first_name="test_first_name",
            last_name="test_last_name",
        )
        self.car = Car.objects.create(
            manufacturer=self.manufacturer, model="test_model"
        )
        self.car.drivers.set([self.driver])

    def test_string_representation(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})",
        )
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}",
        )
        self.assertEqual(str(self.car), self.car.model)

    def test_drivers_get_absolute_url(self):
        expected_url = reverse(
            "taxi:driver-detail",
            kwargs={"pk": self.driver.pk}
        )
        actual_url = self.driver.get_absolute_url()
        self.assertEqual(expected_url, actual_url)
