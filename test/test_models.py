from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Car, Driver


class ManufacturerTest(TestCase):
    def setUp(self):
        self.manufacturer = (
            Manufacturer.objects.create(
                name="Toyota",
                country="Japan"))

    def test_manufacturer_content(self):
        self.assertIsInstance(self.manufacturer.name, str)
        self.assertIsInstance(self.manufacturer.country, str)
        self.assertEqual(str(self.manufacturer), "Toyota Japan")


class CarTest(TestCase):
    def setUp(self):
        self.manufacturer = (
            Manufacturer.objects.create(
                name="Tesla", country="USA"))
        self.driver = Driver.objects.create(
            username="test_driver",
            license_number="ABC12345")
        self.car = Car.objects.create(
            model="Model S",
            manufacturer=self.manufacturer
        )
        self.car.drivers.add(self.driver)

    def test_car_fields(self):
        self.assertIsInstance(self.car.model, str)
        self.assertEqual(self.car.manufacturer.name, "Tesla")
        self.assertIn(self.driver, self.car.drivers.all())


class DriverTest(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create(
            username="johndoe",
            license_number="XYZ789",
            first_name="John",
            last_name="Doe"
        )

    def test_get_absolute_url(self):
        url = reverse("taxi:driver-detail", kwargs={"pk": self.driver.pk})
        self.assertEqual(self.driver.get_absolute_url(), url)
