from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.assertEquals(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_car_str(self):
        car = Car.objects.create(
            model="Model X",
            manufacturer=Manufacturer.objects.create(
                name="Tesla", country="USA"
            ),
        )
        self.assertEquals(str(car), car.model)

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="johnsmith",
            password="Qfd123***",
            license_number="IGD43268",
        )
        self.assertEquals(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})",
        )
