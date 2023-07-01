from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from taxi.models import Car, Manufacturer, Driver


class TestSetUp(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        self.manufacturer_data = {
            "name": "Test Name",
            "country": "Test Country"
        }
        self.manufacturer = Manufacturer.objects.create(
            **self.manufacturer_data
        )
        self.manufacturers = Manufacturer.objects.all()

        self.driver_data = {
            "username": "test.username",
            "password": "password123",
            "first_name": "First",
            "last_name": "Last",
            "license_number": "TES12345",
        }
        self.driver = get_user_model().objects.create_user(**self.driver_data)
        self.drivers = Driver.objects.all()

        self.car_data = {
            "model": "Test Model",
            "manufacturer": self.manufacturer,
        }
        self.car = Car.objects.create(**self.car_data)
        self.car.drivers.add(self.driver)
        self.cars = Car.objects.all()
