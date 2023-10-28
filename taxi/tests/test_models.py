from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW", country="Germany"
        )
        self.assertEquals(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="rambo1982",
            password="JustWantToEatButHaveToKill82",
        )
        self.assertEquals(
            str(driver),
            f"{driver.username} "
            f"({driver.first_name} {driver.last_name})"
        )

    def test_create_driver_with_license(self):
        driver = get_user_model().objects.create(
            username="rambo1982",
            password="JustWantToEatButHaveToKill82",
            license_number="RAM19821"
        )
        self.assertEquals(
            driver.license_number,
            "RAM19821"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Tesla", country="USA"
        )
        car = Car.objects.create(
            model="Model S",
            manufacturer=manufacturer
        )
        self.assertEquals(
            str(car),
            car.model
        )
