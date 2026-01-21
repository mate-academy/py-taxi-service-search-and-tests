from django.test import TestCase

from taxi.models import Manufacturer, Car, Driver


class ModelTests(TestCase):
    def test_manufacturer(self):
        manufacturer = Manufacturer.objects.create(name="Manufacturer", country="USA")
        self.assertEqual(str(manufacturer), f"{manufacturer.name} {manufacturer.country}")

    def test_driver(self):
        driver = Driver.objects.create(
            username="johndoe",
            first_name="John",
            last_name="Doe"
        )
        self.assertEqual(str(driver), f"{driver.username} ({driver.first_name} {driver.last_name})")

    def test_car(self):
        manufacturer = Manufacturer.objects.create(
            name="Mercedes-Benz",
            country="Germany"
        )
        car = Car.objects.create(
            model="Mercedes-Benz A-Class",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), car.model)

    def test_license_number(self):
        driver = Driver.objects.create(
            username="johndoe",
            first_name="John",
            last_name="Doe",
            license_number="Test license number"
        )
        self.assertEqual(driver.license_number, "Test license number")

    def test_driver_get_absolute_url(self):
        driver = Driver.objects.create(
            username="johndoe",
            first_name="John",
            last_name="Doe",
            license_number="XYZ123"
        )
        self.assertEqual(driver.get_absolute_url(), f"/drivers/{driver.pk}/")

