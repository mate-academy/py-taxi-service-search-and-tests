from django.test import TestCase

from taxi.models import Car, Driver, Manufacturer


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )

        self.assertEqual(str(manufacturer), "Toyota Japan")

    def test_driver_str(self):
        driver = Driver.objects.create_user(
            username="test.driver",
            password="testpass123",
            first_name="Test",
            last_name="Driver",
            license_number="ABC12345",
        )

        self.assertEqual(str(driver), "test.driver (Test Driver)")

    def test_driver_get_absolute_url(self):
        driver = Driver.objects.create_user(
            username="test.driver",
            password="testpass123",
            license_number="ABC12345",
        )

        self.assertEqual(
            driver.get_absolute_url(), f"/drivers/{driver.pk}/"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        car = Car.objects.create(model="Camry", manufacturer=manufacturer)

        self.assertEqual(str(car), "Camry")
