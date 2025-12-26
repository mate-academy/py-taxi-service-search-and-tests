from django.test import TestCase

from taxi.models import Manufacturer, Car, Driver


class TestManufacturers(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="ManufacturerTest",
            country="TestUSA",
        )

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name}"
            f" {self.manufacturer.country}"
        )

    def test_manufacturer_search_by_name(self):
        search_results = Manufacturer.objects.filter(
            name__icontains="nufa"
        )
        self.assertEqual(
            search_results.count(),
            1
        )
        self.assertEqual(
            search_results.first().name,
            "ManufacturerTest"
        )


class TestCars(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="ManufacturerTest",
            country="TestUSA",
        )
        self.driver = Driver.objects.create_user(
            license_number="ABS23451",
            username="TestTest",
            first_name="TestFirstName",
            last_name="TestLastName",
            password="test1234",
        )
        self.car = Car.objects.create(
            model="Test",
            manufacturer=self.manufacturer
        )
        self.car.drivers.set([self.driver])

    def test_car_str(self):
        self.assertEqual(
            str(self.car),
            f"{self.car.model}"
        )

    def test_car_search_by_model(self):
        search_results = Car.objects.filter(
            model__icontains="st"
        )
        self.assertEqual(
            search_results.count(),
            1
        )
        self.assertEqual(
            search_results.first().model,
            "Test"
        )


class TestDrivers(TestCase):
    def setUp(self) -> None:
        self.driver = Driver.objects.create_user(
            license_number="ABS23451",
            username="TestTest",
            first_name="TestFirstName",
            last_name="TestLastName",
            password="test1234",
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username}"
            f" ({self.driver.first_name}"
            f" {self.driver.last_name})"
        )

    def test_driver_search_by_username(self):
        search_results = Driver.objects.filter(
            username__icontains="est"
        )
        self.assertEqual(
            search_results.count(),
            1
        )
        self.assertEqual(
            search_results.first().username,
            "TestTest"
        )
