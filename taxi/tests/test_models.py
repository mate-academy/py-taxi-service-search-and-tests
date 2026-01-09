from django.test import TestCase
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer, Car


class ManufacturerModelTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )

    def test_manufacturer_str(self):
        """Test the manufacturer string representation"""
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )

    def test_manufacturer_creation(self):
        """Test manufacturer is created correctly"""
        self.assertTrue(isinstance(self.manufacturer, Manufacturer))
        self.assertEqual(self.manufacturer.name, "Tesla")
        self.assertEqual(self.manufacturer.country, "USA")


class DriverModelTests(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="testdriver",
            password="test12345",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345"
        )

    def test_driver_str(self):
        """Test the driver string representation"""
        expected = (f"{self.driver.username} "
                    f"({self.driver.first_name} {self.driver.last_name})")
        self.assertEqual(str(self.driver), expected)

    def test_driver_get_absolute_url(self):
        """Test driver get_absolute_url method"""
        self.assertEqual(
            self.driver.get_absolute_url(),
            f"/drivers/{self.driver.id}/"
        )

    def test_driver_license_number(self):
        """Test driver has license number"""
        self.assertEqual(self.driver.license_number, "ABC12345")

    def test_create_driver_with_license_number(self):
        """Test creating driver with license number"""
        driver = get_user_model().objects.create_user(
            username="driver2",
            password="test12345",
            license_number="XYZ98765"
        )
        self.assertEqual(driver.license_number, "XYZ98765")


class CarModelTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.driver1 = get_user_model().objects.create_user(
            username="driver1",
            password="test12345",
            license_number="LIC001"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="driver2",
            password="test12345",
            license_number="LIC002"
        )
        self.car = Car.objects.create(
            model="X5",
            manufacturer=self.manufacturer
        )
        self.car.drivers.add(self.driver1, self.driver2)

    def test_car_str(self):
        """Test the car string representation"""
        self.assertEqual(str(self.car), self.car.model)

    def test_car_manufacturer_relationship(self):
        """Test car has correct manufacturer"""
        self.assertEqual(self.car.manufacturer, self.manufacturer)
        self.assertEqual(self.car.manufacturer.name, "BMW")

    def test_car_drivers_relationship(self):
        """Test car has correct drivers"""
        self.assertEqual(self.car.drivers.count(), 2)
        self.assertIn(self.driver1, self.car.drivers.all())
        self.assertIn(self.driver2, self.car.drivers.all())
