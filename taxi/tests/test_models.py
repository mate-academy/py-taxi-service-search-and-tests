from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.models import Manufacturer, Car, Driver


class ModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        username = "Test"
        license_number = "TES12346"
        password = "test123"
        # Set up non-modified objects used by all test methods
        Manufacturer.objects.create(name="Test", country="Testing")
        Car.objects.create(
            model="Test",
            manufacturer=Manufacturer.objects.get(name="Test")
        )
        Driver.objects.create(
            username=username,
            password=password,
            license_number=license_number,
        )

    def test_str_manufacturer(self):
        manufacturer = Manufacturer.objects.create(
            name="Test1",
            country="Testing"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_str_driver(self):
        driver = Driver.objects.create(
            username="Test1",
            first_name="Test",
            last_name="Test",
            license_number="TES12345"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} "
            f"({driver.first_name} {driver.last_name})"
        )

    def test_str_car(self):
        car = Car.objects.create(
            model="Test",
            manufacturer=Manufacturer.objects.get(name="Test")
        )
        self.assertEqual(str(car), str(car.model))

    def test_get_absolute_url_driver(self):
        driver = get_user_model().objects.get(id=1)
        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")
