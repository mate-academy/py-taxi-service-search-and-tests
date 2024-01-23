from django.test import TestCase

from taxi.models import Car, Manufacturer, Driver


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Testerlandia"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = Driver.objects.create(
            username="test",
            password="Test12345",
            first_name="test_name",
            last_name="test_surname"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_create_driver_license_number(self):
        driver = Driver.objects.create_user(
            username="test",
            password="Test12345",
            license_number="ABC12354"
        )
        self.assertEqual(driver.username, "test")
        self.assertEqual(driver.license_number, "ABC12354")
        self.assertTrue(driver.check_password("Test12345"))

    def test_car_str(self):
        driver = Driver.objects.create(
            username="test",
            password="Test12345",
            first_name="test_name",
            last_name="test_surname"
        )
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Testerlandia"
        )
        car = Car.objects.create(
            model="Sambrero",
            manufacturer=manufacturer,
        )
        car.drivers.set([driver])
        self.assertEqual(str(car), car.model)
