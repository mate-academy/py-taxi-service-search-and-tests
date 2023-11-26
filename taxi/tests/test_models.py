from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.driver = Driver.objects.create(
            username="TestUser",
            email="test@user.com",
            password="test123",
            first_name="Test",
            last_name="User",
            license_number="ABC12345",
        )

        cls.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        cls.car = Car.objects.create(
            model="TestModel",
            manufacturer=cls.manufacturer,
        )

        cls.car.drivers.add(
            cls.driver,
        )

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}",
        )

    def test_driver_labels(self):
        verbose_name = self.driver._meta.verbose_name
        verbose_name_plural = self.driver._meta.verbose_name_plural
        self.assertEqual(verbose_name, "driver")
        self.assertEqual(verbose_name_plural, "drivers")

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            (f"{self.driver.username}"
             f" ({self.driver.first_name} {self.driver.last_name})"),
        )

    def test_driver_get_absolute_url(self):
        self.assertEqual(
            self.driver.get_absolute_url(),
            "/drivers/1/",
        )

    def test_car_get_str(self):
        self.assertEqual(
            str(self.car),
            self.car.model,
        )
