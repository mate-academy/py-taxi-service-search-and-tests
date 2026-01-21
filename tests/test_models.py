from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTest(TestCase):
    def test_str_method_for_manufacturer(self):
        manufacturer = Manufacturer.objects.create(name="name",
                                                   country="Italy")
        self.assertEqual(str(manufacturer),
                         f"{manufacturer.name} {manufacturer.country}")

    def test_str_method_for_car(self):
        manufacturer = Manufacturer.objects.create(name="name",
                                                   country="Italy")
        car = Car.objects.create(model="Model X", manufacturer=manufacturer)

        self.assertEqual(str(car), car.model)

    def test_str_method_for_driver(self):
        driver = get_user_model().objects.create_user(
            username="username",
            password="password",
            first_name="first_name",
            last_name="last_name"
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})")
