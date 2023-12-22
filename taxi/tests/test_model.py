from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacture = Manufacturer.objects.create(
            name="Name",
            country="Uk"
        )
        self.assertEquals(
            str(manufacture), f"{manufacture.name} {manufacture.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="Driver",
            password="<PASSWORD>",
            first_name="Test",
            last_name="Test",
        )
        self.assertEquals(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_cart_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Name",
            country="Uk"
        )
        car = Car.objects.create(
            model="test",
            manufacturer=manufacturer
        )
        self.assertEquals(str(car), f"{car.model}")
