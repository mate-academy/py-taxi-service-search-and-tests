from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ManufacturerModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

    def test_manufacturer_creation(self):
        """Test if the manufacturer is created correctly."""
        self.assertEqual(self.manufacturer.name, "Toyota")
        self.assertEqual(self.manufacturer.country, "Japan")

    def test_manufacturer_str(self):
        """Test the __str__ method of the Manufacturer model."""
        self.assertEqual(str(self.manufacturer), "Toyota Japan")

    def test_manufacturer_unique_name(self):
        """Test that the Manufacturer name is unique."""
        with self.assertRaises(Exception):
            Manufacturer.objects.create(name="Toyota", country="USA")


class DriverModelTest(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="john_doe",
            password="testpass123",
            first_name="John",
            last_name="Doe",
            license_number="AB123456"
        )

    def test_driver_creation(self):
        """Test if the driver is created correctly."""
        self.assertEqual(self.driver.username, "john_doe")
        self.assertEqual(self.driver.license_number, "AB123456")

    def test_driver_str(self):
        """Test the __str__ method of the Driver model."""
        self.assertEqual(str(self.driver), "john_doe (John Doe)")

    def test_driver_get_absolute_url(self):
        """Test the get_absolute_url method of the Driver model."""
        self.assertEqual(
            self.driver.get_absolute_url(),
            f"/drivers/{self.driver.pk}/"
        )

    def test_license_number_unique(self):
        """Test that the license number is unique."""
        with self.assertRaises(Exception):
            Driver.objects.create_user(
                username="jane_doe",
                password="testpass123",
                first_name="Jane",
                last_name="Doe",
                license_number="AB123456"  # Duplicate license number
            )


class CarModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Honda",
            country="Japan"
        )
        self.driver = Driver.objects.create_user(
            username="alex_smith",
            password="testpass123",
            first_name="Alex",
            last_name="Smith",
            license_number="XY987654"
        )
        self.car = Car.objects.create(
            model="Civic",
            manufacturer=self.manufacturer
        )
        self.car.drivers.add(self.driver)

    def test_car_creation(self):
        """Test if the car is created correctly."""
        self.assertEqual(self.car.model, "Civic")
        self.assertEqual(self.car.manufacturer.name, "Honda")
        self.assertIn(self.driver, self.car.drivers.all())

    def test_car_str(self):
        """Test the __str__ method of the Car model."""
        self.assertEqual(str(self.car), "Civic")

    def test_car_relationship_with_driver(self):
        """Test ManyToMany relationship between Car and Driver."""
        self.assertEqual(self.car.drivers.count(), 1)
        self.assertIn(self.driver, self.car.drivers.all())
