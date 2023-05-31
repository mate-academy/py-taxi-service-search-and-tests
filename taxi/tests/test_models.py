from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.models import Driver, Manufacturer, Car


class DriverModelTests(TestCase):
    def test_driver_str(self) -> None:
        driver = get_user_model().objects.create_user(
            username="test_user",
            first_name="Test",
            last_name="User",
            password="test12345",
            license_number="ABC12345"
        )
        self.assertEqual(str(driver), "test_user (Test User)")

    def test_license_number_unique(self) -> None:
        get_user_model().objects.create_user(
            username="test_user1",
            password="test12345",
            license_number="ABC12345"
        )

        with self.assertRaises(Exception) as context:
            get_user_model().objects.create_user(
                username="test_user2",
                password="test12345",
                license_number="ABC12345"
            )

        self.assertTrue("UNIQUE" in str(context.exception))


class CarModelTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Manufacturer 1",
            country="Country 1"
        )
        self.driver = Driver.objects.create(
            username="test_user",
            first_name="Test",
            last_name="User",
            license_number="ABC123"
        )
        self.car = Car.objects.create(
            model="Car Model",
            manufacturer=self.manufacturer
        )
        self.car.drivers.add(self.driver)

    def test_car_str(self) -> None:
        car = Car.objects.get(id=self.car.id)
        self.assertEqual(str(car), "Car Model")

    def test_car_manufacturer(self) -> None:
        car = Car.objects.get(id=self.car.id)
        self.assertEqual(car.manufacturer, self.manufacturer)

    def test_car_drivers(self) -> None:
        car = Car.objects.get(id=self.car.id)
        self.assertIn(self.driver, car.drivers.all())

    def test_manufacturer_str(self) -> None:
        manufacturer = Manufacturer.objects.get(id=self.manufacturer.id)
        self.assertEqual(str(manufacturer), "Manufacturer 1 Country 1")


class ManufacturerModelTests(TestCase):
    def test_manufacturer_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Manufacturer 1",
            country="Country 1"
        )
        self.assertEqual(str(manufacturer), "Manufacturer 1 Country 1")
