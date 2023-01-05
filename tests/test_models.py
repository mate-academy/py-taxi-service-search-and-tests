from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        name = "Test name"
        country = "Text country"
        manufacturer = Manufacturer.objects.create(name=name, country=country)

        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        username = "Test name"
        first_name = "Test first name"
        last_name = "Test last name"
        driver = get_user_model().objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        name = "Test name"
        country = "Text country"
        model = "Test name"
        manufacturer = Manufacturer.objects.create(name=name, country=country)
        car = Car.objects.create(model=model, manufacturer=manufacturer)

        self.assertEqual(str(car), car.model)
