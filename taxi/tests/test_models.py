from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class ManufacturerModelTestCase(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer", country="Test Country"
        )

    def test_unique_name(self):
        duplicate_manufacturer = Manufacturer(
            name="Test Manufacturer", country="Another Country"
        )

        with self.assertRaises(Exception):
            duplicate_manufacturer.full_clean()

    def test_str_method(self):
        self.assertEqual(str(self.manufacturer),
                         "Test Manufacturer Test Country")


class DriverModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.driver = Driver.objects.create(
            username="testuser", first_name="Test", last_name="User"
        )

    def test_driver_absolute_url(self):
        driver = Driver.objects.get(username="testuser")

        expected_url = reverse(
            "taxi:driver-detail", kwargs={"pk": driver.pk}
        )

        self.assertEqual(driver.get_absolute_url(), expected_url)


class CarModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer", country="Test Country"
        )

        cls.driver = Driver.objects.create(
            username="testuser", first_name="Test", last_name="User"
        )

        cls.car = Car.objects.create(
            model="Test Car", manufacturer=cls.manufacturer
        )

        cls.car.drivers.add(cls.driver)

    def test_car_model(self):
        car = Car.objects.get(model="Test Car")
        self.assertEqual(str(car), "Test Car")

    def test_car_manufacturer(self):
        car = Car.objects.get(model="Test Car")
        self.assertEqual(car.manufacturer, self.manufacturer)

    def test_car_drivers(self):
        car = Car.objects.get(model="Test Car")
        self.assertIn(self.driver, car.drivers.all())
