from django.test import TestCase

from taxi.models import Driver, Manufacturer, Car


class ModelsTest(TestCase):

    def test_create_driver(self):
        driver = Driver.objects.create_user(
            username="test_driver",
            password="12345",
            license_number="AAA00001"
        )

        self.assertEqual(driver.username, "test_driver")
        self.assertEqual(driver.license_number, "AAA00001")

    def test_create_manufacturer(self):
        manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )

        self.assertEqual(manufacturer.name, "Audi")
        self.assertEqual(manufacturer.country, "Germany")

    def test_create_car(self):
        manufacturer = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )

        car = Car.objects.create(
            model="Focus",
            manufacturer=manufacturer
        )

        self.assertEqual(car.model, "Focus")
        self.assertEqual(car.manufacturer, manufacturer)
