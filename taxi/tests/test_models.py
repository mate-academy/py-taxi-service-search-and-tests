from django.test import TestCase

from ..models import Manufacturer, Driver, Car


class ManufacturerModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer", country="Test Country"
        )

    def test_name_content(self):
        manufacturer = Manufacturer.objects.get(id=self.manufacturer.id)
        expected_object_name = f"{manufacturer.name} {manufacturer.country}"
        self.assertEquals(expected_object_name, str(manufacturer))


class DriverModelTest(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create(
            username="testuser",
            license_number="ABC12345",
            first_name="John",
            last_name="Doe",
        )

    def test_driver_content(self):
        driver = Driver.objects.get(id=self.driver.id)
        expected_object_name = (
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )
        self.assertEquals(expected_object_name, str(driver))


class CarModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer", country="Test Country"
        )
        self.driver = Driver.objects.create(
            username="testuser",
            license_number="ABC12345",
            first_name="John",
            last_name="Doe",
        )
        self.car = Car.objects.create(
            model="Test Model", manufacturer=self.manufacturer
        )
        self.car.drivers.add(self.driver)

    def test_car_content(self):
        car = Car.objects.get(id=self.car.id)
        self.assertEquals(car.model, "Test Model")
        self.assertEquals(car.manufacturer.name, "Test Manufacturer")
        self.assertEquals(car.drivers.count(), 1)
        self.assertEquals(car.drivers.first().username, "testuser")
        self.assertEquals(car.drivers.first().license_number, "ABC12345")
        self.assertEquals(car.drivers.first().first_name, "John")
        self.assertEquals(car.drivers.first().last_name, "Doe")
