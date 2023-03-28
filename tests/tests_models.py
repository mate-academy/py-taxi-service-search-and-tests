from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="bmw3", country="Germany"
        )
        self.driver = get_user_model().objects.create_user(
            username="vasya.pupkin",
            first_name="Vasya",
            last_name="Pupkin",
            password="345ert345",
            license_number="ABC12345",
        )
        self.car = Car.objects.create(
            model="X5",
            manufacturer=self.manufacturer,
        )

    def test_manufacturer_str(self) -> None:
        obj = self.manufacturer
        self.assertEqual(str(obj), "bmw3 Germany")

    def test_car_str(self) -> None:
        obj = self.car
        self.assertEqual(str(obj), obj.model)

    def test_driver_str(self) -> None:
        obj = self.driver
        self.assertEqual(
            str(obj), f"{obj.username} ({obj.first_name} {obj.last_name})"
        )

    def test_driver_get_absolute_url(self):
        driver = self.driver
        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")
