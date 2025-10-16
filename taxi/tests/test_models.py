from django.test import TestCase

from taxi.models import Driver, Car, Manufacturer
from django.contrib.auth import get_user_model

class ModelTests(TestCase):
    def test_driver_str(self):
        User = get_user_model()
        driver = User.objects.create(
            username="test_driver",
            license_number="TST12345",
            first_name="<NAME>",
            last_name="<SURNAME>",
        )
        self.assertEqual(
            str(driver),
            f"{driver.first_name} {driver.last_name}: {driver.license_number}",
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="<TESTMANF>",
            country="US",
        )
        car = Car.objects.create(
            model="<TESTMODEL>",
            manufacturer=manufacturer,
        )
        self.assertEqual(
            str(car),
            f"{manufacturer.name} " f"{manufacturer.country}: " f"{car.model}",
        )

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="<TESTMANF>",
            country="<TESTCOUNTRY>",
        )
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} ({manufacturer.country})"
        )
