import uuid

from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Manufacturer, Car


class ManufacturerModelTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name=f"testmanuf-{uuid.uuid4()}",
            country="testcountry"
        )

        self.driver1 = Driver.objects.create_user(
            username="driver1",
            password="testpass123",
            license_number="ABC12345",
        )
        self.driver2 = Driver.objects.create_user(
            username="driver2",
            password="testpass123",
            license_number="ABC54321",
        )
        self.car = Car.objects.create(
            model="test model",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.set([self.driver1, self.driver2])


class DriverModelTests(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="ABC12345",
            first_name="Test",
            last_name="Test",
        )

    def test_driver_str_method_returns_username_and_full_name(self):
        expected_str = (f"{self.driver.username} "
                        f"({self.driver.first_name} {self.driver.last_name})")
        self.assertEqual(str(self.driver), expected_str)

    def test_driver_returns_correct_absolute_url(self):
        self.assertEqual(
            self.driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": self.driver.pk})
        )


class CarModelsTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="testmanuf", country="testcountry"
        )
        self.driver1 = Driver.objects.create_user(
            username="driver1",
            password="testpass123",
            license_number="ABC12345",
        )
        self.driver2 = Driver.objects.create_user(
            username="driver2",
            password="testpass123",
            license_number="ABC54321",
        )
        self.car = Car.objects.create(
            model="test model",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.set([self.driver1, self.driver2])

    def test_car_str_returns_model(self):
        self.assertEqual(str(self.car), "test model")

    def test_car_drivers_many_to_many_relationship(self):
        drivers = self.car.drivers.all()
        self.assertIn(self.driver1, drivers)
        self.assertIn(self.driver2, drivers)
        self.assertEqual(drivers.count(), 2)
