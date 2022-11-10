from django.test import TestCase
from django.contrib.auth import get_user_model

from taxi.models import (
    Manufacturer,
    Driver,
    Car
)


class ManufacturerModelTest(TestCase):
    
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Honda",
            country="Japan"
        )
        expected_object_name = f"{manufacturer.name} {manufacturer.country}"
        self.assertEqual(str(manufacturer), expected_object_name)


class CarModelTest(TestCase):

    def test_car_str(self):
        car = Car.objects.create(
            model="Civic",
            manufacturer=Manufacturer.objects.create(
                name="Honda", country="Japan"
            )
        )
        self.assertEqual(str(car), car.model)


class DriverModelTest(TestCase):

    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="sandychicks",
            password="123chicks",
            first_name="Sandy",
            last_name="Chicks",
            license_number="JKQ12345",
        )

    def test_driver_str(self):
        self.assertEqual(str(self.driver), "sandychicks (Sandy Chicks)")

    def test_get_absolute_url(self):
        driver = Driver.objects.get(id=1)
        self.assertEqual(driver.get_absolute_url(), '/drivers/1/')

    def test_create_driver_with_license(self):
        self.assertEqual(self.driver.username, "sandychicks")
        self.assertTrue(self.driver.check_password("123chicks"))
        self.assertEqual(self.driver.license_number, "JKQ12345")
