from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_create_manufacturer(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )
        self.assertEqual(manufacturer.name, "test")
        self.assertEqual(manufacturer.country, "test_country")

    def test_create_driver_with_number(self):
        driver = Driver.objects.create_user(
            username="test_user",
            password="test12345",
            license_number="test_license",
        )
        self.assertEqual(driver.license_number, "test_license")

    def test_driver_str(self):
        driver = Driver.objects.create_user(
            username="test_user",
            password="test12345",
            license_number="test_license",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_creation(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )
        driver = Driver.objects.create_user(
            username="test_user",
            password="test12345",
            license_number="test_license",
        )
        car = Car.objects.create(
            model="test_model",
            manufacturer=manufacturer,
        )
        car.drivers.add(driver)
        self.assertEqual(car.model, "test_model")
        self.assertEqual(car.manufacturer, manufacturer)
        self.assertIn(driver, car.drivers.all())

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )
        driver = Driver.objects.create_user(
            username="test_user",
            password="test12345",
            license_number="test_license",
        )
        car = Car.objects.create(
            model="test_model",
            manufacturer=manufacturer,
        )
        car.drivers.add(driver)
        self.assertEqual(str(car), car.model)
