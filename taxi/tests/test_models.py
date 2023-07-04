from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class TestManufacturerModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(name="TestName", country="TestCountry")

    def test_str_method_manufacturer(self):
        manufacturer = Manufacturer.objects.get(id=1)
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )


class TestDriverModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        Driver.objects.create(
            username="TestUsername",
            first_name="TestFirstName",
            last_name="TestLastName",
        )

    def test_str_method_driver(self):
        driver = Driver.objects.get(id=1)
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_absolut_url(self):
        driver = Driver.objects.get(id=1)
        self.assertEqual(driver.get_absolute_url(), f"/drivers/{driver.id}/")


class TestCarModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(name="TestName", country="TestCountry")
        Car.objects.create(
            model="TestModel", manufacturer=Manufacturer.objects.get(id=1)
        )

    def test_str_method_car(self):
        car = Car.objects.get(id=1)
        self.assertEqual(str(car), car.model)
