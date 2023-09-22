from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="test", country="test")
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = Driver.objects.create(
            username="test",
            first_name="test",
            last_name="test"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        car = Car.objects.create(
            model="Test Model",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), car.model)

    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer1",
            country="Test Country"
        )
        self.driver1 = Driver.objects.create(
            license_number="ABC12345"
            , username="Driver 1"
        )
        self.driver2 = Driver.objects.create(
            license_number="ABC12346"
            , username="Driver 2"
        )

    def test_car_manufacturer_relationship(self):
        car = Car.objects.create(
            model="Test Model",
            manufacturer=self.manufacturer
        )

        self.assertEqual(car.manufacturer, self.manufacturer)

    def test_car_drivers_relationship(self):
        car = Car.objects.create(
            model="Test Model",
            manufacturer=self.manufacturer
        )
        car.drivers.add(self.driver1, self.driver2)

        self.assertIn(self.driver1, car.drivers.all())
        self.assertIn(self.driver2, car.drivers.all())

    def test_create_driver_with_license_number(self):
        username = "test"
        license_number = "ABC12348"
        driver = Driver.objects.create(
            username=username,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
