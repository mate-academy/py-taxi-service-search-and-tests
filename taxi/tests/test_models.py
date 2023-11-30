from django.test import TestCase
from taxi.models import Manufacturer, Driver, Car


class ModelsTests(TestCase):
    def setUp(self):
        # Create test data
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        self.driver = Driver.objects.create(
            username="testuser",
            license_number="ABC123"
        )
        self.car = Car.objects.create(
            model="Test Model",
            manufacturer=self.manufacturer
        )

    def test_manufacturer_str_method(self):
        manufacturer = Manufacturer.objects.get(name="Test Manufacturer")
        self.assertEqual(str(manufacturer), "Test Manufacturer Test Country")

    def test_driver_str_method(self):
        driver = Driver.objects.get(username="testuser")
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str_method(self):
        car = Car.objects.get(model="Test Model")
        self.assertEqual(str(car), "Test Model")

    def test_driver_get_absolute_url_method(self):
        driver = Driver.objects.get(username="testuser")
        self.assertEqual(driver.get_absolute_url(), f"/drivers/{driver.pk}/")
