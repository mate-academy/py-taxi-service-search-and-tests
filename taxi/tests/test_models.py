from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class TestManufacturers(TestCase):
    def setUp(self):
        manufacturers_list = [
            {
                "name": "Volkswagen",
                "country": "Germany",
            },
            {
                "name": "Toyota",
                "country": "Japan",
            },
            {
                "name": "Subaru",
                "country": "Japan",
            },
            {
                "name": "Renault",
                "country": "France",
            },
            {
                "name": "Seat",
                "country": "Spain",
            },
        ]
        for manufacturer in manufacturers_list:
            Manufacturer.objects.create(
                name=manufacturer["name"],
                country=manufacturer["country"],
            )

    def test_manufacturers_str(self):
        for manufacturer in Manufacturer.objects.all():
            self.assertEqual(
                str(manufacturer),
                f"{manufacturer.name} {manufacturer.country}"
            )


class TestDrivers(TestCase):
    def setUp(self):
        drivers_list = [
            {
                "username": "test_driver_1",
                "first_name": "Test",
                "last_name": "One",
                "password": "Test1111",
                "license_number": "AAA11111",
            },
            {
                "username": "test_driver_2",
                "first_name": "Test",
                "last_name": "Two",
                "password": "Test2222",
                "license_number": "AAA22222",
            },
            {
                "username": "test_driver_3",
                "first_name": "Test",
                "last_name": "Three",
                "password": "Test3333",
                "license_number": "AAA33333",
            }
        ]
        for driver in drivers_list:
            get_user_model().objects.create_user(
                username=driver["username"],
                first_name=driver["first_name"],
                last_name=driver["last_name"],
                password=driver["password"],
                license_number=driver["license_number"],
            )

    def test_drivers_str(self):
        for driver in Driver.objects.all():
            self.assertEqual(
                str(driver),
                f"{driver.username} ({driver.first_name} {driver.last_name})"
            )


class TestCars(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )
        self.car = Car.objects.create(
            model="E46",
            manufacturer=self.manufacturer,
        )

    def test_cars_str(self):
        self.assertEqual(str(self.car), self.car.model)
