from django.test import TestCase

from taxi.models import Manufacturer, Car, Driver


class ManufacturerModelTest(TestCase):
    def test_manufacturer(self):
        bmw = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        self.assertEqual(str(bmw), f"{bmw.name} {bmw.country}")


class DriverModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Driver.objects.create_user(
            username="driver1",
            password="top_driver",
            first_name="John",
            last_name="Doe"
        )

    def test_driver_str(self):
        driver = Driver.objects.get(id=1)
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_get_absolute_url(self):
        driver = Driver.objects.get(id=1)
        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")


class CarModelTest(TestCase):
    def test_car(self):
        bmw = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        car = Car.objects.create(
            model="M5",
            manufacturer=bmw,
        )

        self.assertEqual(str(car), car.model)
