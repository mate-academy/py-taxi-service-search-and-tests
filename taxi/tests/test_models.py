from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    @classmethod
    def setUp(cls):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )

        Car.objects.create(
            model="test",
            manufacturer=manufacturer
        )

        get_user_model().objects.create(
            username="test",
            first_name="first",
            last_name="last"
        )

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.get(id=1)
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_car_str(self):
        car = Car.objects.get(id=1)
        self.assertEqual(
            str(car),
            car.model
        )

    def test_representation_of_driver(self):
        driver = get_user_model().objects.get(id=1)
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )
