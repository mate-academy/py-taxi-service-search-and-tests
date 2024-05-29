from django.test import TestCase
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer, Car


class ManufacturerModelTests(TestCase):

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name", country="test_country"
        )
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_manufacturer_ordering(self):
        manufacturer1 = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        manufacturer2 = Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(list(manufacturers), [manufacturer2, manufacturer1])


class DriverModelTests(TestCase):

    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test_username",
            password="password123",
            first_name="test_name",
            last_name="test_last_name",
            license_number="12345678",
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})",
        )

    def test_create_driver_with_license_number(self):
        self.assertEqual(self.driver.username, "test_username")
        self.assertEqual(self.driver.license_number, "12345678")
        self.assertTrue(self.driver.check_password("password123"))


class CarModelTests(TestCase):

    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="test_manufacturer_name", country="test_country"
        )
        self.car = Car.objects.create(
            model="test_model", manufacturer=self.manufacturer
        )
        self.driver = get_user_model().objects.create_user(
            username="test_username",
            password="password123",
            first_name="test_first_name",
            last_name="test_last_name",
            license_number="12345678",
        )
        self.car.drivers.add(self.driver)

    def test_car_str(self):
        self.assertEqual(str(self.car), "test_model")

    def test_car_manufacturer_relationship(self):
        self.assertEqual(self.car.manufacturer, self.manufacturer)

    def test_car_drivers_relationship(self):
        self.assertIn(self.driver, self.car.drivers.all())
