from django.test import TestCase
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturers_str(self):
        manufacturer = Manufacturer.objects.create(name="test",
                                                   country="TestCountry")
        self.assertEquals(str(manufacturer), "test TestCountry")

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            license_number="ABC3BC",
            username="test",
            first_name="test",
            last_name="test",
            password="test123"
        )
        self.assertEquals(str(driver),
                          f"{driver.username}"
                          f" ({driver.first_name}"
                          f" {driver.last_name})")

    def test_car_str(self):
        driver = get_user_model().objects.create(
            license_number="ABC3BC",
            username="test",
            first_name="test",
            last_name="test",
            password="test123"
        )
        manufacturer = Manufacturer.objects.create(name="test",
                                                   country="TestCountry")
        car = Car.objects.create(model="testModel", manufacturer=manufacturer)
        car.drivers.add(driver)
        car.save()
        self.assertEquals(str(car), car.model)

    def test_create_driver_with_license_number(self):
        driver = get_user_model().objects.create(
            license_number="ABC3BC",
            username="test",
            first_name="test",
            last_name="test",
            password="test123"
        )
        self.assertEquals(driver.license_number, "ABC3BC")
